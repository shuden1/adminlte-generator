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
    profile_folder_path = os.getenv("CHROME_PROFILE_PATH") + "\\" + str(threading.get_ident())
    service = Service(executable_path=r""+os.getenv("CHROME_DRIVER_PATH")+"")

    options = Options()
    options.add_argument(f"user-data-dir={profile_folder_path}")
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")

    driver = webdriver.Chrome(service=service, options=options)

    try:
        driver.get(f"file:///{file_path}")

        job_blocks = driver.find_elements(By.CSS_SELECTOR, 'div.acb-position-container a.acb-position')
        job_listings = []

        for job_block in job_blocks:
            job_title = job_block.find_element(By.CSS_SELECTOR, 'h4').text
            job_url = job_block.get_attribute('href')
            job_listings.append({"Job-title": job_title, "URL": job_url})

        print(json.dumps(job_listings, indent=4))

    finally:
        driver.quit()

if __name__ == "__main__":
    file_path = sys.argv[1]
    scrape_jobs(file_path)
