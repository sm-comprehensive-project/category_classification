from celery import Celery
from config import REDIS_URL

# Celery 인스턴스 생성
celery_app = Celery("category_tasks", broker=REDIS_URL, backend=REDIS_URL)

# 이 디렉토리 내의 task 모듈 자동 인식
celery_app.autodiscover_tasks(['task_queue_module'])  # <- 디렉토리명 정확히!
