from task_queue_module.task_queue import celery_app
from crawler.dispatcher import route_to_parser
from crawler.fetch_html import create_driver
from crawler.utils import preprocess_row_dict
from model.classify import predict_category
@celery_app.task
def test_process(doc_id, url):
    driver = create_driver()
    try:
        result = route_to_parser(url, driver)
        processed_text = preprocess_row_dict(result)
        result['processed_text'] = processed_text  # 👈 다음 단계에 넘기기 위해 추가
        # 3️⃣ 예측
        category = predict_category(processed_text)
        result['Category'] = category  # 👈 다음 단계에 넘기기 위해 추가
        print(f"🧪 전처리 결과: {processed_text}")

        # (다음 단계: 분류 및 DB 저장 예정)
        return result
    
    finally:
        driver.quit()
