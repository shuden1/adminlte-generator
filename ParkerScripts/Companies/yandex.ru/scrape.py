import sys
import json
import threading
from selenium import webdriver
import os
from dotenv import load_dotenv

load_dotenv()
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException

def scrape_jobs(file_path):
    profile_folder_path = os.getenv("CHROME_PROFILE_PATH") + "\\" + str(threading.get_ident())
    service = Service(executable_path=r""+os.getenv("CHROME_DRIVER_PATH")+"")

    options = webdriver.ChromeOptions()
    options.add_argument(f"user-data-dir={profile_folder_path}")
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")

    driver = webdriver.Chrome(service=service, options=options)

    try:
        driver.get(f"file:///{file_path}")

        job_openings = []

        job_elements = driver.find_elements(By.CSS_SELECTOR, 'span.lc-jobs-vacancy-card[data-vacancy-card="true"]')

        for job_element in job_elements:
            try:
                title_element = job_element.find_element(By.CSS_SELECTOR, 'div.lc-jobs-text.lc-jobs-text_type_header.lc-jobs-vacancy-card__header')
                title = title_element.text.strip() if title_element.text.strip() else title_element.get_attribute('innerHTML').strip()
            except NoSuchElementException:
                title = "No Title"

            try:
                url_element = job_element.find_element(By.CSS_SELECTOR, 'a.Link.lc-jobs-link')
                url = url_element.get_attribute('href').strip() if url_element.get_attribute('href').strip() else "#"
            except NoSuchElementException:
                url = "#"

            job_openings.append({"Job-title": title, "URL": url})

        print(json.dumps(job_openings, ensure_ascii=False))

    finally:
        driver.quit()

if __name__ == "__main__":
    file_path = sys.argv[1]
    scrape_jobs(file_path)
