# task_queue.py
# 🔧 Celery 애플리케이션을 초기화하고, 태스크 모듈들을 자동으로 탐색하도록 설정하는 중심 파일

from celery import Celery
from config import REDIS_URL  # Redis 브로커 주소 설정

# ✅ Celery 인스턴스 생성
# - "category_tasks"는 워커 이름을 지정
# - broker: 작업 전송용 Redis
# - backend: 작업 결과 저장용 Redis
celery_app = Celery("category_tasks", broker=REDIS_URL, backend=REDIS_URL)

# ✅ 태스크 자동 등록: 지정된 모듈에서 @task 붙은 함수 자동 검색
# 단, 복잡한 구조에서는 자동 등록이 누락될 수 있음
celery_app.autodiscover_tasks(['task_queue_module'])

# ✅ 누락 방지를 위한 명시적 import (실제로는 여기서 task 함수가 실행되지는 않음)
# - Celery가 이 모듈들 안의 태스크를 등록하게 됨
import task_queue_module.crawl_task
import task_queue_module.infer_task
