import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import pickle
import os

# ✅ 1. 사전 정의된 경로에서 모델 관련 파일 로드
from config import MODEL_PATH  # 모델 디렉토리 (ex: "./results")

# ✅ 2. 토크나이저 & 분류 모델 로드 (로컬에서만 불러오도록 설정)
try:
    tokenizer = AutoTokenizer.from_pretrained(MODEL_PATH, local_files_only=True)
    model = AutoModelForSequenceClassification.from_pretrained(MODEL_PATH, local_files_only=True)
    # ✅ 3. label_encoder.pkl 로드 (예측된 ID → 라벨 이름으로 변환하는 데 사용)
    # - 학습 시 LabelEncoder().fit(y_train) 후 저장해둔 객체
    with open(f"{MODEL_PATH}/label_encoder.pkl", "rb") as f:
        label_encoder = pickle.load(f)

except Exception as e:
    print(f"❌ 모델 로딩 실패: {e}")
    raise RuntimeError("모델 초기화 실패")

# ✅ 4. 분류 예측 함수 정의
# - 입력 텍스트를 모델 입력 포맷으로 변환 → 예측 수행 → 결과 ID → 라벨로 변환
def predict_category(text: str) -> str:
    try:
        if not isinstance(text, str) or not text.strip():
            raise ValueError("입력 텍스트가 비어 있거나 유효하지 않습니다.")

        inputs = tokenizer(text, return_tensors="pt", truncation=True, padding=True)

        # 모델 예측 수행
        outputs = model(**inputs)

        # 예측된 클래스 ID
        pred_id = torch.argmax(outputs.logits, dim=1).item()

        # ID → 라벨 이름 변환
        label = label_encoder.inverse_transform([pred_id])[0]
        return label

    except Exception as e:
        print(f"❌ 예측 실패: {e}")
        return "기타"  # 또는 fallback label, 또는 raise
