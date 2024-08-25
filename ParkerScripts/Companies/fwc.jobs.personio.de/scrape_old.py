import sys
import json
import threading
from selenium import webdriver
import os
from dotenv import load_dotenv

load_dotenv()
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

def scrape_jobs(file_path):
    profile_folder_path = os.getenv("CHROME_PROFILE_PATH") + os.path.sep + str(threading.get_ident())
    service = Service(executable_path=r""+os.getenv("CHROME_DRIVER_PATH")+"")

    options = Options()
    options.add_argument(f"user-data-dir={profile_folder_path}")
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")

    driver = webdriver.Chrome(service=service, options=options)

    driver.get(f"file:///{file_path}")

    job_opening_selector = 'section.job-category-wrapper.all-tab-category-wrapper'
    job_title_selector = 'a'
    job_url_selector = 'a'

    job_elements = driver.find_elements(By.CSS_SELECTOR, job_opening_selector)

    job_listings = []
    for job_element in job_elements:
        job_title = job_element.find_element(By.CSS_SELECTOR, job_title_selector).text.strip()
        job_url = job_element.find_element(By.CSS_SELECTOR, job_url_selector).get_attribute('href')
        job_listings.append({"Job-title": job_title, "URL": job_url})

    driver.quit()

    return json.dumps(job_listings, indent=4)

if __name__ == "__main__":
    file_path = sys.argv[1]
    print(scrape_jobs(file_path))
