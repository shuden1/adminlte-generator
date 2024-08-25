import sys
import json
import threading
from selenium import webdriver
import os
from dotenv import load_dotenv

load_dotenv()
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException

def scrape_jobs(file_path):
    profile_folder_path = os.getenv("CHROME_PROFILE_PATH") + "\\" + str(threading.get_ident())
    service = Service(executable_path=r""+os.getenv("CHROME_DRIVER_PATH")+"")
    options = Options()
    options.add_argument(f"user-data-dir={profile_folder_path}")
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")

    driver = webdriver.Chrome(service=service, options=options)
    driver.get(f"file:///{file_path}")

    job_listings = []

    try:
        job_elements = driver.find_elements(By.CSS_SELECTOR, "div.t778__col.t-col.t-col_8.t-prefix_2.t-align_left.t-item.js-product")
        for job_element in job_elements:
            try:
                title_element = job_element.find_element(By.CSS_SELECTOR, "div.t778__title.t-name.t-name_md.js-product-name")
                title = title_element.text.strip() if title_element.text.strip() else title_element.get_attribute('innerHTML').strip()
            except NoSuchElementException:
                title = "No Title Found"

            try:
                url_element = job_element.find_element(By.CSS_SELECTOR, "a")
                url = url_element.get_attribute('href') if url_element.get_attribute('href') else "#"
            except NoSuchElementException:
                url = "#"

            job_listings.append({"Job-title": title, "URL": url})
    except NoSuchElementException:
        pass

    driver.quit()
    return json.dumps(job_listings, ensure_ascii=False)

if __name__ == "__main__":
    file_path = sys.argv[1]
    print(scrape_jobs(file_path))
