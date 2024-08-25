import sys
from selenium import webdriver
import os
from dotenv import load_dotenv

load_dotenv()
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
import threading
import json

def scrape_job_listings(file_name):
    profile_folder_path = f"{os.getenv("CHROME_PROFILE_PATH")}{os.path.sep}{str(threading.get_ident())}"
    service = ChromeService(executable_path=r""+os.getenv("CHROME_DRIVER_PATH")+"")
    options = webdriver.ChromeOptions()
    options.add_argument(f"user-data-dir={profile_folder_path}")
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    driver = webdriver.Chrome(service=service, options=options)

    try:
        driver.get(f"file:///{file_name}")
        job_elements = driver.find_elements(By.CSS_SELECTOR, ".awsm-job-post-title a")
        jobs_list = []
        for job in job_elements:
            jobs_list.append({"Job-title": job.text, "URL": job.get_attribute('href')})
        return json.dumps(jobs_list)
    finally:
        driver.quit()

if __name__ == "__main__":
    file_name = sys.argv[1]
    print(scrape_job_listings(file_name))
