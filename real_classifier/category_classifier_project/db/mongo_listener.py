from pymongo import MongoClient
from pymongo.errors import PyMongoError
from config import MONGO_URI
from task_queue_module.tasks import test_process
from datetime import datetime

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

                # Redis로 연결된 Celery 작업 큐에 태스크 전달
                test_process.delay(doc_id)

    except PyMongoError as e:
        print(f"❌ MongoDB change stream 오류: {e}")

if __name__ == "__main__":
    listen_for_changes()
