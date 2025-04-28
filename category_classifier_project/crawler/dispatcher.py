import requests
from crawler.parser_gift import parse_gift
from crawler.parser_deal import parse_deal
from utils.logging import log
from config import FASTAPI_NAVER_SERVER

def route_to_parser(url: str, driver):
    log.info("🔍 URL 라우팅 시작", extra={"url": url})

    try:
        if "gift.kakao.com" in url:
            log.info("🎁 gift.kakao.com 파싱 호출")
            return parse_gift(url, driver)

        elif "store.kakao.com" in url:
            log.info("🛒 store.kakao.com 파싱 호출")
            return parse_deal(url, driver)

        elif "smartstore.naver.com" in url:
            log.info("🌐 smartstore FastAPI 서버 요청", extra={"endpoint": FASTAPI_NAVER_SERVER})
            try:
                res = requests.post(FASTAPI_NAVER_SERVER, json={"url": url}, timeout=10)
                res.raise_for_status()
                return res.json()
            except Exception as e:
                log.exception("❌ 네이버 크롤링 서버 요청 실패", extra={"url": url})
                return None

        else:
            log.warning("❌ 지원하지 않는 URL 형식", extra={"url": url})
            return None

    except Exception as e:
        log.exception("❌ route_to_parser 내부 예외 발생", extra={"url": url})
        return None
