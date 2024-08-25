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

        job_openings = driver.find_elements(By.CSS_SELECTOR, "div.col-12.py-2.hideshow-jobtype.jobtype-filter")

        jobs = []
        for job in job_openings:
            title_element = job.find_element(By.CSS_SELECTOR, "h1, h2, h3, h4, h5, h6, p, a")
            title = title_element.text
            url_element = job.find_element(By.CSS_SELECTOR, "a[href]")
            url = url_element.get_attribute("href")

            jobs.append({"Job-title": title, "URL": url})

        print(json.dumps(jobs, indent=4))

    finally:
        driver.quit()

if __name__ == "__main__":
    file_path = sys.argv[1]
    scrape_jobs(file_path)
