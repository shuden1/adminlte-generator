from selenium import webdriver
import os
from dotenv import load_dotenv

load_dotenv()
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import shutil
import threading
import sys
import json

job_listings_selector = ".job-listings .visible.opportunity"
job_title_selector = "h4.listing-title"
job_url_selector = "a.listing-link"

def scrape_jobs(html_file):
    profile_folder_path = os.getenv("CHROME_PROFILE_PATH") + "\\" + str(threading.get_ident())

    try:
        chrome_options = Options()
        chrome_options.add_argument(f"user-data-dir={profile_folder_path}")
        chrome_options.add_argument("--headless")

        service = ChromeService(executable_path=r""+os.getenv("CHROME_DRIVER_PATH")+"")

        driver = webdriver.Chrome(service=service, options=chrome_options)
        driver.get(f"file://{html_file}")

        jobs = driver.find_elements(By.CSS_SELECTOR, job_listings_selector)

        job_data = []
        for job in jobs:
            title_element = job.find_element(By.CSS_SELECTOR, job_title_selector)
            url_element = job.find_element(By.CSS_SELECTOR, job_url_selector)
            job_data.append({
                "Job-title": title_element.text,
                "URL": url_element.get_attribute('href')
            })

        print(json.dumps(job_data))

    finally:
        driver.quit()


if __name__ == "__main__":
    html_file = sys.argv[1]
    scrape_jobs(html_file)
