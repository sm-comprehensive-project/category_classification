from pymongo import MongoClient
from pymongo.errors import PyMongoError
from config import MONGO_URI
from utils.logging import log  # ✅ 공통 로거
# ✅ 변경: crawl_task에서 불러오기
from task_queue_module.crawl_task import crawl_product

def extract_url_from_product(product: dict) -> str:
    return product.get("link", "")

def listen_for_changes():
    client = MongoClient(MONGO_URI)
    db = client["damoa"]
    collection = db["kakao_product"]

    try:
        with collection.watch([{"$match": {"operationType": "insert"}}]) as stream:
            log.info("🔔 MongoDB change stream 감지 시작")

            for change in stream:
                doc = change["fullDocument"]
                doc_id = str(doc["_id"])
                log.info("📥 새 document 감지됨", extra={"doc_id": doc_id})

                products = doc.get("products", [])
                if not products:
                    log.warning("⚠️ products가 비어 있음", extra={"doc_id": doc_id})
                    continue

                for idx, product in enumerate(products):
                    url = extract_url_from_product(product)
                    if url:
                        log.info("➡️ Celery 작업 전송", extra={
                            "doc_id": doc_id,
                            "product_index": idx,
                            "url": url
                        })
                        crawl_product.delay(doc_id, product)
                    else:
                        log.warning("⚠️ product에 유효한 링크 없음", extra={
                            "doc_id": doc_id,
                            "product_index": idx
                        })

    except PyMongoError as e:
        log.exception("❌ MongoDB change stream 오류")

if __name__ == "__main__":
    listen_for_changes()
