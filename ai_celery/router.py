from configs.env import settings
from ai_celery.init_broker import is_broker_running
from ai_celery.init_redis import is_backend_running
from ai_celery.celery_app import app

if not is_backend_running():
    exit()
if not is_broker_running():
    exit()

app.conf.task_routes = {
    'tasks.ai_lip_sync_task': {'queue': settings.AI_LIP_SYNC},
}

from ai_celery.ai_lip_sync import ai_lip_sync_task
