import sys
from selenium import webdriver
import os
from dotenv import load_dotenv

load_dotenv()
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
import threading
import json

def scrape_job_listings(html_file):
    profile_folder_path = os.getenv("CHROME_PROFILE_PATH") + "\\" + str(threading.get_ident())
    service = ChromeService(executable_path=r"C:\\Python3\\chromedriver.exe")
    options = webdriver.ChromeOptions()
    options.add_argument(f"user-data-dir={profile_folder_path}")
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")

    driver = webdriver.Chrome(service=service, options=options)
    driver.get(f"file:///{html_file}")

    jobs_data = []
    job_listings = driver.find_elements(By.CSS_SELECTOR, '.job-listing a')
    for job_listing in job_listings:
        job_title = job_listing.text.strip()
        job_url = job_listing.get_attribute('href')

        if job_title and job_url:
            jobs_data.append({"Job-title": job_title, "URL": job_url})

    driver.quit()
    return json.dumps(jobs_data, ensure_ascii=False)

if __name__ == "__main__":
    html_file_path = sys.argv[1]
    print(scrape_job_listings(html_file_path))
