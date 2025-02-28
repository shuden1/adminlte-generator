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

def scrape_jobs(html_file_path):
    profile_folder_path = os.getenv("CHROME_PROFILE_PATH") + os.path.sep + str(threading.get_ident())
    service = Service(executable_path=r""+os.getenv("CHROME_DRIVER_PATH")+"")

    options = Options()
    options.add_argument(f"user-data-dir={profile_folder_path}")
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")

    driver = webdriver.Chrome(service=service, options=options)

    driver.get(f"file:///{html_file_path}")

    job_openings = []

    # Use the selectors identified in STEP 1
    job_blocks = driver.find_elements(By.CSS_SELECTOR, 'div[class*="INSERT_CORRECT_JOB_BLOCK_CLASS"]')  # Replace with correct selector

    for job_block in job_blocks:
        job_title_element = job_block.find_element(By.CSS_SELECTOR, 'a[class*="INSERT_CORRECT_JOB_TITLE_CLASS"]')  # Replace with correct selector
        job_url_element = job_title_element

        job_title = job_title_element.text
        job_url = job_url_element.get_attribute('href')

        job_openings.append({"Job-title": job_title, "URL": job_url})

    driver.quit()

    return json.dumps(job_openings, indent=4)

if __name__ == "__main__":
    html_file_path = sys.argv[1]
    print(scrape_jobs(html_file_path))
