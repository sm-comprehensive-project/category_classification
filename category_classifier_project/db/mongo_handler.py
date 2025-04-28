from pymongo import MongoClient
from pymongo.errors import PyMongoError
from config import MONGO_URI
from utils.logging import log

def save_classified_product(doc_id: str, product: dict, category: str):
    """
    분류 결과(category)를 포함한 product 정보를 MongoDB에 저장하는 함수
    """
    try:
        client = MongoClient(MONGO_URI)
        db = client["damoa"]
        collection = db["classified_product"]

        # 카테고리 추가
        product["Category"] = category
        product["source_doc_id"] = doc_id  # 원본 doc_id 기록

        # 저장
        result = collection.insert_one(product)
        print(product)
         # ✅ 성공 로그
        log.info("✅ MongoDB 저장 완료", extra={
            "doc_id": doc_id,
            "category": category,
            "inserted_id": str(result.inserted_id)
        })
    except PyMongoError as e:
        log.exception(f"❌ MongoDB 저장 중 오류 발생: {e}")
    finally:
        client.close()