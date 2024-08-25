import sys
import json
import shutil
import threading
from selenium import webdriver
import os
from dotenv import load_dotenv

load_dotenv()
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By

def main(html_file_path):
    profile_folder_path = f"{os.getenv("CHROME_PROFILE_PATH")}{os.path.sep}{threading.get_ident()}"
    os.makedirs(profile_folder_path, exist_ok=True)

    service_instance = Service(executable_path=r""+os.getenv("CHROME_DRIVER_PATH")+"")
    options = webdriver.ChromeOptions()
    options.add_argument(f"user-data-dir={profile_folder_path}")
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")

    driver = webdriver.Chrome(service=service_instance, options=options)
    driver.get(f"file:///{html_file_path}")

    # Exact selectors should be identified in STEP 1. Here using placeholders based on typical patterns.
    job_listing_selector = '.job-listing, .job-opening, .opening, .position'
    job_title_url_selector = 'h2 > a, h3 > a, .job-title > a, .title > a'

    job_openings = driver.find_elements(By.CSS_SELECTOR, job_listing_selector)
    results = []

    for job in job_openings:
        title_elements = job.find_elements(By.CSS_SELECTOR, job_title_url_selector)
        for title_element in title_elements:
            results.append({
                "Job-title": title_element.text.strip(),
                "URL": title_element.get_attribute('href').strip()
            })

    driver.quit()
    # shutil.rmtree(profile_folder_path, ignore_errors=True)

    return json.dumps(results, indent=2)

if __name__ == "__main__":
    output = main(sys.argv[1])
    print(output)
