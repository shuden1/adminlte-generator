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

        job_opening_selector = "table.srJobList tr.srJobListJobOdd, table.srJobList tr.srJobListJobEven"
        job_title_selector = "td.srJobListJobTitle"
        job_url_attribute = "onclick"

        job_elements = driver.find_elements(By.CSS_SELECTOR, job_opening_selector)
        job_listings = []

        for job_element in job_elements:
            job_title_element = job_element.find_element(By.CSS_SELECTOR, job_title_selector)
            job_title = job_title_element.text.strip()
            job_url = job_element.get_attribute(job_url_attribute).split('"')[1]

            job_listings.append({
                "Job-title": job_title,
                "URL": job_url
            })

        print(json.dumps(job_listings, indent=4))

    finally:
        driver.quit()

if __name__ == "__main__":
    file_path = sys.argv[1]
    scrape_jobs(file_path)
