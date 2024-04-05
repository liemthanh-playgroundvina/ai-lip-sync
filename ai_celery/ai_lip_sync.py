import json
import os.path

from celery import Task
from ai_celery.celery_app import app
from configs.env import settings
from ai_celery.common import Celery_RedisClient, CommonCeleryService

from scripts.wav2lip.w2l import W2l
from scripts.wav2lip.wav2lip_uhq import Wav2LipUHQ
from moviepy.editor import VideoFileClip, AudioFileClip, CompositeAudioClip


class AILipSyncTask(Task):
    """
    Abstraction of Celery's Task class to support AI Lip Sync
    """
    abstract = True

    def __init__(self):
        super().__init__()

    def __call__(self, *args, **kwargs):
        return self.run(*args, **kwargs)


@app.task(
    bind=True,
    base=AILipSyncTask,
    name="{query}.{task_name}".format(
        query=settings.AI_QUERY_NAME,
        task_name=settings.AI_LIP_SYNC
    ),
    queue=settings.AI_LIP_SYNC
)
def ai_lip_sync_task(self, task_id: str, data: bytes, task_request: bytes, file: bytes):
    """
    Service AI Lip Sync tasks

    task_request example:
        file: {
            'audio_voice': {'content_type': 'audio/mpeg', 'filename': 'static/public/ai_cover_gen/2024_03_28_07_36_55_479_mama.mp3'},
            'audio_background': {'content_type': 'audio/mpeg', 'filename': 'static/public/ai_cover_gen/2024_03_28_07_36_55_479_mama.mp3'},
            'video': {'content_type': 'video/mp4', 'filename': 'static/public/ai_cover_gen/2024_03_28_07_36_55_479_mama.mp4'},

        }
    """
    print("============= AI Lip Sync task: Started ===================")
    try:
        # Load data
        data = json.loads(data)
        request = json.loads(task_request)
        file = json.loads(file)
        Celery_RedisClient.started(task_id, data)

        # Request
        voice_path = file.get('audio_voice')['filename'].split('/')[-1]
        voice_path = os.path.join("/app/static/public/ai_cover_gen", voice_path)
        background_path = file.get('audio_background')['filename'].split('/')[-1]
        background_path = os.path.join("/app/static/public/ai_cover_gen", background_path)
        video_path = file.get('video')['filename'].split('/')[-1]
        video_path = os.path.join("/app/static/public/ai_cover_gen", video_path)
        print(video_path, voice_path, background_path)

        # Predict
        wav2lip_file = generate(video_path, voice_path, background_path)
        print(wav2lip_file)

        # Save s3
        url_file = CommonCeleryService.upload_s3_file(
            wav2lip_file,
            "video/mp4",
            settings.AI_COVER_GEN
        )
        # Successful
        metadata = {
            "task": "ai_lip_sync",
            "tool": "local",
            "model": "wav2lip",
            "usage": None,
        }
        response = {"url_file": url_file, "metadata": metadata}
        Celery_RedisClient.success(task_id, data, response)
        return

    except Exception as e:
        print(str(e))
        err = {'code': "500", 'message': "Internal Server Error"}
        Celery_RedisClient.failed(task_id, data, err)
        return


def generate(video, audio, background_audio):
    if video is None or audio is None:
        raise ValueError("[ERROR] Please select a video and an audio file")

    resize_factor = 1

    w2l = W2l(video, audio, "wav2lip", False, resize_factor, 0, 0, 0, 0, None)
    w2l.execute()

    w2luhq = Wav2LipUHQ(video, "GFPGAN", 15, 15, 15,
                        False, None, resize_factor, 0.75, False)

    wav2lip_file_name = os.path.splitext(os.path.basename(audio))[0] + ".mp4"
    response = w2luhq.execute(wav2lip_file_name=wav2lip_file_name)

    # Add background audio
    video_clip = VideoFileClip(response[-1])
    audio_clip = AudioFileClip(background_audio)

    composite_audio = CompositeAudioClip([video_clip.audio, audio_clip])
    video_clip.audio = composite_audio

    video_clip.write_videofile(wav2lip_file_name)

    return wav2lip_file_name
