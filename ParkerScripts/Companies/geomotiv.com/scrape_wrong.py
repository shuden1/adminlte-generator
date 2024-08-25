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

        job_openings = driver.find_elements(By.CSS_SELECTOR, 'select[aria-hidden="false"][data-ajax="1"][data-allow_null="0"][data-multiple="0"][data-placeholder="Select"][data-ui="1"]')
        jobs = []

        for job_opening in job_openings:
            try:
                job_title_element = job_opening.find_element(By.CSS_SELECTOR, 'option[data-i="0"][selected="selected"]')
                job_title = job_title_element.text.strip() or job_title_element.get_attribute('innerHTML').strip()

                job_url_element = job_opening.find_element(By.CSS_SELECTOR, 'a')
                job_url = job_url_element.get_attribute('href') if job_url_element else "#"

                jobs.append({"Job-title": job_title, "URL": job_url})
            except NoSuchElementException:
                continue

        print(json.dumps(jobs, indent=4))

    finally:
        driver.quit()

if __name__ == "__main__":
    html_file_path = sys.argv[1]
    scrape_jobs(html_file_path)
