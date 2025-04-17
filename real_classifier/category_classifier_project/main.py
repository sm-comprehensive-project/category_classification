# main.py
from pymongo import MongoClient
from pymongo.errors import PyMongoError
from task_queue_module.tasks import test_process
from config import MONGO_URI

def listen_for_changes():
    client = MongoClient(MONGO_URI)
    db = client["damoa"]
    collection = db["kakao_product"]

    try:
        with collection.watch([{"$match": {"operationType": "insert"}}]) as stream:
            print("🔔 MongoDB change stream 감지 시작")

            for change in stream:
                doc = change["fullDocument"]
                doc_id = str(doc["_id"])
                print(f"📥 새 document 감지됨: {doc_id}")

                # ✅ products가 있고, 첫 번째 상품에 link가 있을 때만 전송
                if doc.get("products") and doc["products"][0].get("link"):
                    url = doc["products"][0]["link"]
                    test_process.delay(doc_id, url)
                else:
                    print("⚠️ products가 없거나 link가 없음")

    except PyMongoError as e:
        print(f"❌ MongoDB change stream 오류: {e}")

if __name__ == "__main__":
    listen_for_changes()
