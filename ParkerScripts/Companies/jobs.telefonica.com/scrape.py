from bs4 import BeautifulSoup
import json
import sys
import threading
from selenium import webdriver
import os
from dotenv import load_dotenv

load_dotenv()
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By

# STEP 1 Output:
job_block_selector = "tr.data-row"
job_title_selector = "td.colTitle span.jobTitle a.jobTitle-link"
job_url_selector = "td.colTitle span.jobTitle a.jobTitle-link"

# STEP 2 Script:
def scrape_job_listings(html_file_name):
    service = ChromeService(executable_path=r""+os.getenv("CHROME_DRIVER_PATH")+"")
    profile_folder_path = f"{os.getenv("CHROME_PROFILE_PATH")}{os.path.sep}{str(threading.get_ident())}"
    options = webdriver.ChromeOptions()
    options.add_argument(f"user-data-dir={profile_folder_path}")
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")

    driver = webdriver.Chrome(service=service, options=options)

    try:
        driver.get(f"file://{html_file_name}")
        job_elements = driver.find_elements(By.CSS_SELECTOR, job_block_selector)
        jobs = []
        for job_element in job_elements:
            title_element = job_element.find_element(By.CSS_SELECTOR, job_title_selector)
            title = title_element.text
            url = job_element.find_element(By.CSS_SELECTOR, job_url_selector).get_attribute('href')
            jobs.append({"Job-title": title, "URL": url})
        return json.dumps(jobs)

    finally:
        driver.quit()

if __name__ == "__main__":
    html_file_name = sys.argv[1]
    print(scrape_job_listings(html_file_name))
