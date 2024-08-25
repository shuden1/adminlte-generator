import threading
import shutil
from selenium import webdriver
import os
from dotenv import load_dotenv

load_dotenv()
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
import json
import sys

# STEP 1 results
job_block_selector = ".card.card-job"
job_title_selector = ".card-title a"

# STEP 2 script
def scrape_job_listings(html_file_name):
    profile_folder_path = os.getenv("CHROME_PROFILE_PATH") + os.path.sep + str(threading.get_ident())
    service = ChromeService(executable_path=r""+os.getenv("CHROME_DRIVER_PATH")+"")
    options = webdriver.ChromeOptions()
    options.add_argument(f"user-data-dir={profile_folder_path}")
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")

    driver = webdriver.Chrome(service=service, options=options)
    driver.get(f"file://{html_file_name}")

    job_elements = driver.find_elements(By.CSS_SELECTOR, job_block_selector)
    job_listings = []
    for job_element in job_elements:
        title_element = job_element.find_element(By.CSS_SELECTOR, job_title_selector)
        job_listings.append({
            "Job-title": title_element.text,
            "URL": title_element.get_attribute("href")
        })

    driver.quit()


    return json.dumps(job_listings)

if __name__ == "__main__":
    html_file_name = sys.argv[1]
    print(scrape_job_listings(html_file_name))
