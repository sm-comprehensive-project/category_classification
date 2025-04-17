from fastapi import FastAPI
from pydantic import BaseModel
from selenium import webdriver
from selenium.webdriver.common.by import By
from contextlib import asynccontextmanager
import time
import json

app = FastAPI()

# ✅ 전역 드라이버 (FastAPI 서버 시작 시 생성됨)
driver = None

# ✅ 드라이버 설정
def start_driver():
    options = webdriver.ChromeOptions()
    options.add_argument('--start-maximized')
    options.add_argument('--disable-blink-features=AutomationControlled')
    options.add_argument('--disable-gpu')
    options.add_argument('--window-size=1920,1080')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    return webdriver.Chrome(options=options)

# ✅ 서버 시작 시 드라이버 켜기
@asynccontextmanager
async def lifespan(app: FastAPI):
    global driver
    driver = start_driver()   # 서버 시작 시 드라이버 실행
    print("✅ 드라이버 실행됨")
    yield
    driver.quit()             # 서버 종료 시 드라이버 종료
    print("🛑 드라이버 종료됨")

app = FastAPI(lifespan=lifespan)

# ✅ 요청 형식
class CrawlRequest(BaseModel):
    url: str

# ✅ 크롤링 엔드포인트
@app.post("/crawl")
def crawl_url(req: CrawlRequest):
    global driver
    try:
        driver.get("https://shopping.naver.com/")
        time.sleep(1)
        driver.get(req.url)
        time.sleep(2)

        product_name, price, detail_info = "", "", {}

        url = req.url
        if "luxury/boutique" in url:
            product_name = driver.find_element(By.CSS_SELECTOR, "#content h3").text.strip()
            price = driver.find_element(By.CSS_SELECTOR, "span._1LY7DqCnwR").text.strip()
            tables = driver.find_elements(By.CSS_SELECTOR, "#INTRODUCE table.TH_yvPweZa")
            for table in tables:
                for row in table.find_elements(By.TAG_NAME, "tr"):
                    ths = row.find_elements(By.CSS_SELECTOR, "th._15qeGNn6Dt")
                    tds = row.find_elements(By.CSS_SELECTOR, "td.jvlKiI0U_y")
                    for th, td in zip(ths, tds):
                        detail_info[th.text.strip()] = td.text.strip()

        elif "smartstore" in url:
            product_name = driver.find_element(By.CSS_SELECTOR, "#content h3").text.strip()
            price = driver.find_element(By.CSS_SELECTOR, "span._1LY7DqCnwR").text.strip()
            tables = driver.find_elements(By.CSS_SELECTOR, "div._copyable > table._1_UiXWHt__")
            for table in tables:
                for row in table.find_elements(By.TAG_NAME, "tr"):
                    ths = row.find_elements(By.CSS_SELECTOR, "th._1iuv6pLHMD")
                    tds = row.find_elements(By.CSS_SELECTOR, "td.ABROiEshTD")
                    for th, td in zip(ths, tds):
                        key = th.text.strip()
                        detail_info[key] = td.text.strip()

        elif "window-products" in url:
            product_name = driver.find_element(By.CSS_SELECTOR, "#content h3").text.strip()
            price = driver.find_element(By.CSS_SELECTOR, "span._1LY7DqCnwR").text.strip()
            tables = driver.find_elements(By.CSS_SELECTOR, "#INTRODUCE table.TH_yvPweZa")
            for table in tables:
                for row in table.find_elements(By.TAG_NAME, "tr"):
                    ths = row.find_elements(By.CSS_SELECTOR, "th._15qeGNn6Dt")
                    tds = row.find_elements(By.CSS_SELECTOR, "td.jvlKiI0U_y")
                    for th, td in zip(ths, tds):
                        detail_info[th.text.strip()] = td.text.strip()

        return {
            "Product_Name": product_name,
            "Price": price,
            "Detail_Info": json.dumps(detail_info, ensure_ascii=False)
        }

    except Exception as e:
        return {"error": str(e)}

# ✅ 서버 종료 시 드라이버 종료
@app.on_event("shutdown")
def shutdown_event():
    global driver
    if driver:
        driver.quit()
        print("🛑 드라이버 종료됨")
