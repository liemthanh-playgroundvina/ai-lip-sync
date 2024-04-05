# AI LIP SYNC
- Link: https://github.com/numz/sd-wav2lip-uhq

- Queue System using celery(python) + redis + rabbitMQ

- Image information: Python 3.11


1. Clone & download model
```# command
git clone https://github.com/liemthanh-playgroundvina/ai-lip-sync
cd ai-lip-sync
make download_model
```

2. Build Image
```# command
make build
```

3. Start
```# command
make start
```