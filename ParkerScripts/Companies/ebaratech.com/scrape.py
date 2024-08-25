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

        job_postings = []

        rows = driver.find_elements(By.CSS_SELECTOR, "tr")
        for row in rows:
            try:
                title_element = row.find_element(By.CSS_SELECTOR, "td")
                job_title = title_element.text.strip() or title_element.get_attribute('innerHTML').strip()

                try:
                    url_element = row.find_element(By.CSS_SELECTOR, "a")
                    job_url = url_element.get_attribute('href').strip()
                except NoSuchElementException:
                    job_url = "#"

                job_postings.append({"Job-title": job_title, "URL": job_url})
            except NoSuchElementException:
                continue

        print(json.dumps(job_postings, indent=4))

    finally:
        driver.quit()

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script.py <path_to_html_file>")
        sys.exit(1)

    file_path = sys.argv[1]
    scrape_jobs(file_path)
