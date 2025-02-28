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

def scrape_jobs(html_file_path):
    profile_folder_path = os.getenv("CHROME_PROFILE_PATH") + os.path.sep + str(threading.get_ident())
    service = Service(executable_path=r""+os.getenv("CHROME_DRIVER_PATH")+"")

    options = webdriver.ChromeOptions()
    options.add_argument(f"user-data-dir={profile_folder_path}")
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")

    driver = webdriver.Chrome(service=service, options=options)

    try:
        driver.get(f"file:///{html_file_path}")

        job_openings = driver.find_elements(By.CSS_SELECTOR, 'span.text-block-base-link.sm\\:min-w-\\[25\\%\\].sm\\:truncate.company-link-style')
        jobs = []

        for job in job_openings:
            try:
                job_title = job.text.strip()
                if not job_title:
                    job_title = job.get_attribute('innerHTML').strip()

                job_url_element = job.find_element(By.XPATH, './ancestor::a')
                job_url = job_url_element.get_attribute('href')
                if not job_url:
                    job_url = "#"

                jobs.append({"Job-title": job_title, "URL": job_url})
            except NoSuchElementException:
                continue

        print(json.dumps(jobs, indent=4))

    finally:
        driver.quit()

if __name__ == "__main__":
    html_file_path = sys.argv[1]
    scrape_jobs(html_file_path)
