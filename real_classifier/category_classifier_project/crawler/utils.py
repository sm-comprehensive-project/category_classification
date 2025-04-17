# crawler/utils.py
import json

excluded_values = ['해당없음', '상세', '해당사항', '판매원', '인증', '번호', '기타']
excluded_keys = ['소비자 상담 관련 전화번호', 'A/S', '원산지', '제조', '품질', '에너지', '통신판매', '청약철회']

def preprocess_row_dict(row: dict) -> str:
    product_name = str(row.get('Product_Name', ''))
    price = str(row.get('Price', ''))
    detail_info_raw = str(row.get('Detail_Info', '')).strip()

    try:
        detail_info = json.loads(detail_info_raw)
        filtered_details = []
        for key, value in detail_info.items():
            if any(ex in value for ex in excluded_values):
                continue
            if any(ex in key for ex in excluded_keys):
                continue
            filtered_details.append(f"{key}: {value}")
        detail_text = " / ".join(filtered_details)
    except Exception:
        detail_text = detail_info_raw  # 파싱 실패 시 원본 사용

    return f"제품명: {product_name} / 가격: {price}원" + (f" / {detail_text}" if detail_text else "")
