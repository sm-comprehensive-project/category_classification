# infer_task.py
# 🧠 BERT 기반 분류 모델을 이용해 크롤링된 상품 데이터를 분류하는 태스크 정의

from task_queue_module.task_queue import celery_app  # Celery 인스턴스 import
from crawler.utils import preprocess_row_dict, preprocess_fallback_title_only        # 전처리 함수
from model.classify import predict_category          # BERT 예측 함수
from db.mongo_handler import save_classified_product # 결과를 DB에 저장

# ✅ "inference_queue"에서 실행될 태스크 정의
# - 크롤링된 결과를 받아 전처리하고, 예측 모델을 통해 카테고리를 판단
# - 최종적으로 MongoDB에 저장
@celery_app.task(queue="inference_queue", bind=True, autoretry_for=(Exception,), retry_kwargs={"max_retries": 3}, retry_backoff=True)
def process_inference(self, doc_id: str, product: dict, crawled_result: dict | None):
    try:
        if crawled_result is not None:
            processed_text = preprocess_row_dict(crawled_result)
        else:
            processed_text = preprocess_fallback_title_only(product)

        category = predict_category(processed_text)

        # ✅ 예외가 나더라도 이건 None 방지용
        if crawled_result is None:
            crawled_result = {}

        crawled_result['Category'] = category

        save_classified_product(doc_id, product, category)

    except Exception as e:
        print(f"❌ 분류 태스크 실패: {e}")
        raise e  # Celery에 예외를 알려줘야 재시도됨 (autoretry_for 쓰는 경우)