import sys
import json
import threading
from selenium import webdriver
import os
from dotenv import load_dotenv

load_dotenv()
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By

def scrape_job_listings(html_file_name):
    profile_folder_path = os.getenv("CHROME_PROFILE_PATH") + os.path.sep + str(threading.get_ident())
    service = ChromeService(executable_path=r""+os.getenv("CHROME_DRIVER_PATH")+"")
    options = webdriver.ChromeOptions()
    options.add_argument(f"user-data-dir={profile_folder_path}")
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")

    driver = webdriver.Chrome(service=service, options=options)
    driver.get(f"file:///{html_file_name}")

    job_listings = driver.find_elements(By.CSS_SELECTOR, ".ci-list-module-content.ci-job-list .ci-list-module-title")

    jobs = []
    for job in job_listings:
        job_title = job.text
        job_url = job.get_attribute('href')
        jobs.append({"Job-title": job_title, "URL": job_url})

    driver.quit()
    return json.dumps(jobs)

if __name__ == "__main__":
    html_file_name = sys.argv[1]
    print(scrape_job_listings(html_file_name))
