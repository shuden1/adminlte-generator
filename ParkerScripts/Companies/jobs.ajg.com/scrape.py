import sys
import json
import threading
from selenium import webdriver
import os
from dotenv import load_dotenv

load_dotenv()
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException

def scrape_jobs(html_file_path):
    profile_folder_path = os.getenv("CHROME_PROFILE_PATH") + "\\" + str(threading.get_ident())
    service = Service(executable_path=r""+os.getenv("CHROME_DRIVER_PATH")+"")

    options = Options()
    options.add_argument(f"user-data-dir={profile_folder_path}")
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")

    driver = webdriver.Chrome(service=service, options=options)

    try:
        driver.get(f"file:///{html_file_path}")

        job_elements = driver.find_elements(By.CSS_SELECTOR, 'span[_ngcontent-ewk-c163][itemprop="title"]')

        job_listings = []

        for job_element in job_elements:
            try:
                job_title = job_element.text.strip()
                if not job_title:
                    job_title = job_element.get_attribute('innerHTML').strip()

                job_url_element = job_element.find_element(By.XPATH, './ancestor::a')
                job_url = job_url_element.get_attribute('href') if job_url_element else "#"

                job_listings.append({"Job-title": job_title, "URL": job_url})
            except NoSuchElementException:
                job_listings.append({"Job-title": job_title, "URL": "#"})

        print(json.dumps(job_listings, indent=4))

    finally:
        driver.quit()

if __name__ == "__main__":
    html_file_path = sys.argv[1]
    scrape_jobs(html_file_path)
