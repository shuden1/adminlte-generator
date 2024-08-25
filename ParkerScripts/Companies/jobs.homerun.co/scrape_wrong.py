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

def scrape_jobs(file_path):
    profile_folder_path = os.getenv("CHROME_PROFILE_PATH") + os.path.sep + str(threading.get_ident())
    service = Service(executable_path=r""+os.getenv("CHROME_DRIVER_PATH")+"")

    options = Options()
    options.add_argument(f"user-data-dir={profile_folder_path}")
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")

    driver = webdriver.Chrome(service=service, options=options)

    try:
        driver.get(f"file:///{file_path}")

        job_opening_blocks_selector = 'div[data-job-opening]'
        job_title_selector = 'h2 a'

        job_blocks = driver.find_elements(By.CSS_SELECTOR, job_opening_blocks_selector)
        job_postings = []

        for block in job_blocks:
            job_elements = block.find_elements(By.CSS_SELECTOR, job_title_selector)
            for job_element in job_elements:
                job_title = job_element.text.strip()
                job_url = job_element.get_attribute('href')
                if job_title and job_url:
                    job_postings.append({"Job-title": job_title, "URL": job_url})

        print(json.dumps(job_postings, indent=4))

    finally:
        driver.quit()

if __name__ == "__main__":
    file_path = sys.argv[1]
    scrape_jobs(file_path)
