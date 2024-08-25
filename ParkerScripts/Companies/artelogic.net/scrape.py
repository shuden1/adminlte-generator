import sys
from selenium import webdriver
import os
from dotenv import load_dotenv

load_dotenv()
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
import threading
import json

def scrape_job_listings(target_html_file):
    profile_folder_path = os.getenv("CHROME_PROFILE_PATH") + os.path.sep + str(threading.get_ident())
    service = ChromeService(executable_path=r""+os.getenv("CHROME_DRIVER_PATH")+"")
    options = webdriver.ChromeOptions()
    options.add_argument(f"user-data-dir={profile_folder_path}")
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    driver = webdriver.Chrome(service=service, options=options)
    driver.get(f"file:///{target_html_file}")

    job_listings = []
    elements = driver.find_elements(By.CSS_SELECTOR, ".career-positions__list .career-positions__item")
    for element in elements:
        title_element = element.find_element(By.CSS_SELECTOR, ".career-positions__item-entry-title")
        job_title = title_element.text.strip()
        job_url = title_element.get_attribute("href")
        job_listings.append({"Job-title": job_title, "URL": job_url})

    driver.quit()
    return json.dumps(job_listings, ensure_ascii=False)

if __name__ == "__main__":
    target_html_file = sys.argv[1]
    print(scrape_job_listings(target_html_file))
