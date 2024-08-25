import shutil
import threading
from selenium import webdriver
import os
from dotenv import load_dotenv

load_dotenv()
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
import json
import sys

# STEP 1
# Exact HTML selectors for job openings.
job_listings_selector = ".job-listing .job-preview"
job_title_selector = ".job-content h5 a"
job_url_selector = ".job-content h5 a"

# Step 2
def scrape_job_listings(html_filename):
    profile_folder_path = os.getenv("CHROME_PROFILE_PATH") + "\\" + str(threading.get_ident())
    service = ChromeService(executable_path=r""+os.getenv("CHROME_DRIVER_PATH")+"")

    options = webdriver.ChromeOptions()
    options.add_argument(f"user-data-dir={profile_folder_path}")
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")

    driver = webdriver.Chrome(service=service, options=options)
    try:
        driver.get(f"file:///{html_filename}")

        job_blocks = driver.find_elements(By.CSS_SELECTOR, job_listings_selector)
        job_listings = []

        for job_block in job_blocks:
            title_element = job_block.find_element(By.CSS_SELECTOR, job_title_selector)
            job_title = title_element.text
            job_url = title_element.get_attribute('href')
            job_listings.append({"Job-title": job_title, "URL": job_url})

        return json.dumps(job_listings)

    finally:
        driver.quit()


# Read HTML file from command-line argument
html_filename = sys.argv[1]
print(scrape_job_listings(html_filename))
