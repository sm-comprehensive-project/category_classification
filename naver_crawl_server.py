from fastapi import FastAPI
from pydantic import BaseModel
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import json

class CrawlRequest(BaseModel):
    url: str

# ✅ 드라이버 설정 함수
def start_driver():
    options = webdriver.ChromeOptions()
    options.add_argument('--start-maximized')
    options.add_argument('--disable-blink-features=AutomationControlled')
    options.add_argument('--disable-gpu')
    options.add_argument('--window-size=1920,1080')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    return webdriver.Chrome(options=options)

app = FastAPI()

@app.post("/crawl")
def crawl_url(req: CrawlRequest):
    driver = start_driver()
    try:
        print(f"📡 크롤링 요청 URL: {req.url}")
        driver.get("https://shopping.naver.com/")
        time.sleep(1)
        driver.get(req.url)
        time.sleep(2)

        product_name, price, detail_info = "", "", {}
        url = req.url

        if "luxury/boutique" in url or "window-products" in url:
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
                        detail_info[th.text.strip()] = td.text.strip()

        else:
            print("❌ 지원하지 않는 URL 형식입니다.")
            return None

        return {
            "Product_Name": product_name,
            "Price": price,
            "Detail_Info": json.dumps(detail_info, ensure_ascii=False)
        }

    except Exception as e:
        print(f"❌ 크롤링 실패: {e}")
        return None

    finally:
        driver.quit()  # ✅ 요청 끝날 때 드라이버 종료
