import json
import os
import shutil
import sys
import threading
from selenium import webdriver
import os
from dotenv import load_dotenv

load_dotenv()
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By

def scrape(html_file_name):
    profile_folder_path = os.getenv("CHROME_PROFILE_PATH") + "\\" + str(threading.get_ident())
    service = Service(executable_path=r""+os.getenv("CHROME_DRIVER_PATH")+"")
    options = webdriver.ChromeOptions()
    options.add_argument(f"user-data-dir={profile_folder_path}")
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")

    driver = webdriver.Chrome(service=service, options=options)

    try:
        driver.get(f"file:///{html_file_name}")

        job_listings = []
        jobs = driver.find_elements(By.CSS_SELECTOR, ".css-1q2dra3 .css-19uc56f")
        for job in jobs:
            job_listings.append({
                "Job-title": job.text,
                "URL": job.get_attribute('href').replace('file:///D:/', '/')
            })

        return json.dumps(job_listings)

    finally:
        driver.quit()


if __name__ == "__main__":
    html_file_path = sys.argv[1]
    extracted_jobs = scrape(html_file_path)
    print(extracted_jobs)
