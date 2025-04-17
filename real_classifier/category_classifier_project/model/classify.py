import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import pickle
import os
# 1️⃣ 모델 & 토크나이저 로드
from config import MODEL_PATH

MODEL_PATH = os.path.abspath("/home/ubuntu/gaon/final_project/category_classifier_project/models")  # 또는 전체 경로 지정
tokenizer = AutoTokenizer.from_pretrained(MODEL_PATH)
model = AutoModelForSequenceClassification.from_pretrained(MODEL_PATH)

# 2️⃣ 라벨 인코더 로드
with open(f"{MODEL_PATH}/label_encoder.pkl", "rb") as f:
    label_encoder = pickle.load(f)

# 3️⃣ 예측 함수
def predict_category(text: str) -> str:
    inputs = tokenizer(text, return_tensors="pt", truncation=True, padding=True)
    outputs = model(**inputs)
    pred_id = torch.argmax(outputs.logits, dim=1).item()
    label = label_encoder.inverse_transform([pred_id])[0]
    return label
