# crawl_task.py
# 🌐 상품 페이지를 크롤링하여 필요한 정보를 추출하고, 추론 태스크로 넘기는 역할을 함

from task_queue_module.task_queue import celery_app       # Celery 인스턴스
from crawler.dispatcher import route_to_parser            # URL 라우팅 → 크롤링 파서 결정
from crawler.fetch_html import create_driver              # 셀레니움 크롬 드라이버 생성기
from task_queue_module.infer_task import process_inference # 추론 큐로 결과 넘김

# ✅ "crawl_queue"에서 실행될 태스크 정의
# - URL에 따라 Kakao Gift, Kakao Store, Naver Smartstore 등에서 크롤링 수행
@celery_app.task(queue="crawl_queue", bind=True, autoretry_for=(Exception,), retry_kwargs={"max_retries": 3}, retry_backoff=True)
def crawl_product(self, doc_id: str, product: dict):
    url = product.get("link")
    driver = create_driver()

    try:
        result = route_to_parser(url, driver)  # ✅ 이 함수가 None을 반환할 수도 있음

        # 🚨 fallback 처리 없이 inference 호출 가능 (inference 내부에서 처리하니까)
        process_inference.delay(doc_id, product, result)

    except Exception as e:
        print(f"❌ 크롤링 태스크 실패 (doc_id: {doc_id}, url: {url}) → {e}")
        raise e  # autoretry_for을 위해 반드시 raise

    finally:
        driver.quit()
