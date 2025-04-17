import requests
from crawler.parser_gift import parse_gift
from crawler.parser_deal import parse_deal

FASTAPI_NAVER_SERVER = "http://192.168.0.23:8000/crawl"  # ← 여기를 바꿔주세요 (예: 192.168.0.101)

def route_to_parser(url: str, driver):
    if "gift.kakao.com" in url:
        return parse_gift(url, driver)
    elif "store.kakao.com" in url:
        return parse_deal(url, driver)
    elif "smartstore.naver.com" in url:
        try:
            print(f"🌐 POST 요청 → {FASTAPI_NAVER_SERVER}")
            res = requests.post(FASTAPI_NAVER_SERVER, json={"url": url}, timeout=10)
            res.raise_for_status()
            return res.json()
        except Exception as e:
            print(f"❌ 네이버 크롤링 서버 요청 실패: {e}")
            return {
                "Product_Name": "없음",
                "Price": "없음",
                "Category": "없음",
                "Detail_Info": "{}",
            }
    else:
        raise ValueError(f"❌ 지원하지 않는 URL 형식입니다: {url}")