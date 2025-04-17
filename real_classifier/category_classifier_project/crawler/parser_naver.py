import time
from selenium import webdriver
from selenium.webdriver.common.by import By
import json

def parse_naver(url: str, driver):
    try:
        # 네이버 쇼핑 홈 → 타겟 URL 이동
        driver.get("https://smartstore.naver.com")
        time.sleep(2)
        driver.get(url)
        time.sleep(5)

        product_name, price, detail_info = "", "", {}

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

        print("\n✅ parse_naver 완료:")
        print("상품명:", product_name)
        print("가격:", price)

        return {
            "Product_Name": product_name,
            "Price": price,
            "Category": "없음",
            "Detail_Info": json.dumps(detail_info, ensure_ascii=False),
            "url": url,
        }

    except Exception as e:
        print(f"❌ parse_naver 크롤링 실패: {e}")
        return {
            "Product_Name": "없음",
            "Price": "없음",
            "Category": "없음",
            "Detail_Info": "{}",
            "url": url
        }
