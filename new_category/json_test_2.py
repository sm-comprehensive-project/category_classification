import json
import pandas as pd
import concurrent.futures  # 병렬 실행을 위한 라이브러리
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup

# ✅ 1️⃣ 크롬 옵션 설정
chrome_options = Options()
chrome_options.add_argument("--headless=new")  # 최신 Headless 모드 (속도 향상)
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--log-level=3")
chrome_options.add_argument("--window-size=1920x1080")
chrome_options.add_argument("--disable-blink-features=AutomationControlled")
chrome_options.add_argument("--blink-settings=imagesEnabled=false")
chrome_options.add_argument("--disable-extensions")
chrome_options.add_argument("--disable-infobars")

# ✅ 2️⃣ JSON 파일에서 URL 가져오기
json_file_path = "kakao_url.json"  # JSON 파일 경로
with open(json_file_path, "r", encoding="utf-8") as file:
    data = json.load(file)

# ✅ 3️⃣ store.kakao.com에서만 URL 추출
urls = [product["link"] for entry in data if "products" in entry for product in entry["products"] if "link" in product and product["link"].startswith("https://store.kakao.com")]

# ✅ 4️⃣ 크롤링 실행 함수 (병렬 실행)
def crawl_category(url):
    """각 URL을 크롤링하여 카테고리 정보를 가져오는 함수"""
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)

    driver.get(url)

    # 🚀 WebDriverWait으로 요소가 로드될 때까지 기다림
    try:
        WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "#mArticle > div > div.product_section > app-view-product-category-path > div > div > a"))
        )
    except:
        print(f"❌ 요소를 찾을 수 없습니다: {url}")
        driver.quit()
        return {"URL": url, "카테고리 전체 경로": "없음"}

    # ✅ BeautifulSoup으로 HTML 파싱
    html = driver.page_source
    soup = BeautifulSoup(html, "html.parser")

    # ✅ 모든 카테고리 정보 가져오기
    category_elements = soup.select("#mArticle > div > div.product_section > app-view-product-category-path > div > div > a")

    # ✅ 텍스트만 추출하여 리스트로 저장
    categories = [category.text.strip() for category in category_elements]

    # ✅ 카테고리 전체 경로 (첫 번째 열)
    category_full_path = " > ".join(categories)

    # ✅ 딕셔너리 형태로 저장 (카테고리 개수 유동적 대응)
    category_dict = {"URL": url, "카테고리 전체 경로": category_full_path}
    print(category_dict)
    # ✅ 개별 카테고리 열 추가 (유동적)
    for i, category in enumerate(categories):
        category_dict[f"카테고리_{i+1}"] = category

    driver.quit()
    return category_dict

# ✅ 5️⃣ 병렬 처리 (최대 5개씩 동시 실행)
results = []
with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
    futures = {executor.submit(crawl_category, url): url for url in urls}
    for future in concurrent.futures.as_completed(futures):
        results.append(future.result())

# ✅ 6️⃣ DataFrame으로 변환 (상품별 카테고리 개수 다름을 고려)
df = pd.DataFrame(results)

# ✅ 7️⃣ CSV 파일 저장
df.to_csv("카테고리_경로.csv", index=False, encoding="utf-8-sig")

# ✅ 🔟 출력 확인
print("✅ 크롤링 완료! 저장된 데이터:")
print(df.head())
