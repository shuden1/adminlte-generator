from selenium import webdriver
import os
from dotenv import load_dotenv

load_dotenv()
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
import threading
import shutil
import json
import sys

# STEP 1: Define selectors
job_list_selector = ".css-1q2dra3"
job_title_selector = "h3 > a.css-19uc56f"
job_url_attribute = "href"

# STEP 2: Create Selenium script
def extract_job_listings(html_file_path):
    profile_folder_path = os.getenv("CHROME_PROFILE_PATH") + os.path.sep + str(threading.get_ident())
    service = ChromeService(executable_path=r""+os.getenv("CHROME_DRIVER_PATH")+"")
    options = webdriver.ChromeOptions()
    options.add_argument(f"user-data-dir={profile_folder_path}")
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")

    driver = webdriver.Chrome(service=service, options=options)

    driver.get(f"file:///{html_file_path}")

    job_listings = []

    job_elements = driver.find_elements(By.CSS_SELECTOR, job_list_selector)
    for job_element in job_elements:
        job_title = job_element.find_element(By.CSS_SELECTOR, job_title_selector).text
        job_url = job_element.find_element(By.CSS_SELECTOR, job_title_selector).get_attribute(job_url_attribute)
        job_listings.append({"Job-title": job_title, "URL": job_url})

    driver.quit()


    return json.dumps(job_listings)

if __name__ == "__main__":
    html_file_path = sys.argv[1] if len(sys.argv) > 1 else ""
    print(extract_job_listings(html_file_path))
