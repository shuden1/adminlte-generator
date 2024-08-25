import sys
from selenium import webdriver
import os
from dotenv import load_dotenv

load_dotenv()
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import threading
import shutil
import json

def scrape_job_listings(html_file_path):
    # Define selectors for job blocks
    job_block_selector = ".jobs-list-item"
    job_title_url_selector = "[data-ph-at-id='job-link']"

    # Step 2: Initialize Chrome in headless mode.
    chrome_options = Options()
    chrome_options.add_argument("--headless")

    profile_folder_path = os.getenv("CHROME_PROFILE_PATH") + "\\" \
                          + str(threading.get_ident())

    chrome_options.add_argument(f"user-data-dir={profile_folder_path}")
    service = ChromeService(executable_path=r""+os.getenv("CHROME_DRIVER_PATH")+"")

    driver = webdriver.Chrome(service=service, options=chrome_options)

    # Step 3: Open the HTML file.
    driver.get(f"file:///{html_file_path}")

    # Step 4: Scrape job listings.
    job_elements = driver.find_elements(By.CSS_SELECTOR, job_block_selector)
    job_listings = []

    for job_elem in job_elements:
        title_elem = job_elem.find_element(By.CSS_SELECTOR, job_title_url_selector)
        job_title = title_elem.text.strip()
        job_url = title_elem.get_attribute('href')
        job_listings.append({"Job-title": job_title, "URL": job_url})

    # Step 5: Return JSON of job listings.
    job_listings_json = json.dumps(job_listings)

    # Step 6: Clean up by closing the driver and removing the profile folder.
    driver.quit()


    return job_listings_json

if __name__ == "__main__":
    html_filename = sys.argv[1]
    print(scrape_job_listings(html_filename))
