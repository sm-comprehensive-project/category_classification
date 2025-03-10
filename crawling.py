from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import pandas as pd
import json

# 웹드라이버 설정 (Chrome 사용)
options = webdriver.ChromeOptions()
#options.add_argument("--headless")  # 브라우저 창 안 띄우기
options.add_argument("--disable-gpu")  
options.add_argument("--no-sandbox")  
options.add_argument("--disable-dev-shm-usage")

# 크롬 드라이버 실행
driver = webdriver.Chrome(options=options)

# 카테고리별 URL 매핑
category_urls = {
    "패션 의류": [
        "https://search.shopping.naver.com/ns/category/10000107",
        "https://search.shopping.naver.com/ns/category/10000108"
    ],
    "화장품_미용": ["https://search.shopping.naver.com/ns/category/10000111"],
    "식품": [
        "https://search.shopping.naver.com/ns/category/10006530",
        "https://search.shopping.naver.com/ns/category/10000114",
        "https://search.shopping.naver.com/ns/category/10000115"
    ],
    "디지털_가전": ["https://search.shopping.naver.com/ns/category/10000120"],
    "가구_인테리어": ["https://search.shopping.naver.com/ns/category/10000112"],
    "출산_육아": ["https://search.shopping.naver.com/ns/category/10000116"],
    "스포츠_레저": ["https://search.shopping.naver.com/ns/category/10000123"],
    "생활_건강": ["https://search.shopping.naver.com/ns/category/10000124"]
}

# 크롤링할 횟수 설정
SCROLL_PAUSE_TIME = 2  # 스크롤 후 대기 시간
MAX_SCROLLS = 20  # 최대 스크롤 횟수

# 카테고리별 크롤링 실행
for category, urls in category_urls.items():
    all_products = []  # 각 카테고리별 데이터 저장

    for url in urls:
        driver.get(url)
        time.sleep(3)  # 페이지 로딩 대기

        # 스크롤 반복
        for _ in range(MAX_SCROLLS):
            driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.END)  # 페이지 끝까지 스크롤
            time.sleep(SCROLL_PAUSE_TIME)  # 로딩 대기

        # 상품 정보 가져오기
        products = driver.find_elements(By.CSS_SELECTOR, "ul.compositeCardList_product_list__Ih4JR > li > div > a")

        for product in products:
            href = product.get_attribute("href")  # 상품 링크
            data_attr = product.get_attribute("data-shp-contents-dtl")  # JSON 형태의 상품 정보
            
            if data_attr:
                try:
                    json_data = json.loads(data_attr)  # 문자열을 JSON으로 변환
                    product_name = next((item["value"] for item in json_data if item["key"] == "prod_nm"), None)
                    if product_name:
                        all_products.append({"Product Name": product_name, "Product Link": href})
                except json.JSONDecodeError:
                    continue  # JSON 파싱 오류 발생 시 무시

    # 데이터 저장
    if all_products:
        df = pd.DataFrame(all_products)
        file_name = f"{category}.csv"  # 카테고리명으로 파일 저장
        df.to_csv(file_name, index=False, encoding="utf-8-sig")

# 크롤링 종료
driver.quit()
