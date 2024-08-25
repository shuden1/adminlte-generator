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

def scrape_job_listings(file_name):
    profile_folder_path = os.getenv("CHROME_PROFILE_PATH") + "\\" + str(threading.get_ident())
    service = Service(executable_path=r""+os.getenv("CHROME_DRIVER_PATH")+"")

    options = webdriver.ChromeOptions()
    options.add_argument(f"user-data-dir={profile_folder_path}")
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")

    driver = webdriver.Chrome(service=service, options=options)

    try:
        driver.get(f"file:///{file_name}")

        job_listings = []

        job_openings = driver.find_elements(By.CSS_SELECTOR, "div.job-opening")

        for job in job_openings:
            try:
                job_title_element = job.find_element(By.CSS_SELECTOR, "h2.job-title")
                job_title = job_title_element.text.strip() or job_title_element.get_attribute('innerHTML').strip()
            except NoSuchElementException:
                job_title = "No Title"

            try:
                job_url_element = job.find_element(By.CSS_SELECTOR, "a.job-url")
                job_url = job_url_element.get_attribute('href') or "#"
            except NoSuchElementException:
                job_url = "#"

            job_listings.append({"Job-title": job_title, "URL": job_url})

        print(json.dumps(job_listings, indent=4))

    finally:
        driver.quit()

if __name__ == "__main__":
    file_name = sys.argv[1]
    scrape_job_listings(file_name)
