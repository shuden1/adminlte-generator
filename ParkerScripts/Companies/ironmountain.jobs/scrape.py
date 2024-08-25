import json
import shutil
import threading
from selenium import webdriver
import os
from dotenv import load_dotenv

load_dotenv()
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
import sys

# Job listings CSS Selectors from STEP 1
job_listing_selector = ".default_jobListing .direct_joblisting"
job_title_selector = "h4 a span.resultHeader"
job_url_selector = "h4 a"

def get_job_listings(driver):
    job_listings = driver.find_elements(By.CSS_SELECTOR, job_listing_selector)
    jobs_data = []

    for job in job_listings:
        title_element = job.find_element(By.CSS_SELECTOR, job_title_selector)
        url_element = job.find_element(By.CSS_SELECTOR, job_url_selector)
        jobs_data.append({
            "Job-title": title_element.text,
            "URL": url_element.get_attribute('href')
        })

    return jobs_data

def main(file_name):
    profile_folder_path = f"{os.getenv("CHROME_PROFILE_PATH")}{os.path.sep}{str(threading.get_ident())}"
    service = ChromeService(executable_path=r""+os.getenv("CHROME_DRIVER_PATH")+"")
    options = webdriver.ChromeOptions()
    options.add_argument(f"user-data-dir={profile_folder_path}")
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")

    driver = webdriver.Chrome(service=service, options=options)
    driver.get(f"file:///{file_name}")

    try:
        job_listings = get_job_listings(driver)
        print(json.dumps(job_listings))
    finally:
        driver.quit()


if __name__ == "__main__":
    html_file_name = sys.argv[1]
    main(html_file_name)
