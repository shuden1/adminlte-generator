from selenium import webdriver
import os
from dotenv import load_dotenv

load_dotenv()
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import threading
import shutil
import sys
import os
import json

# Selectors based on provided structure
job_block_selector = ".card.card-contact-small.card-gray.card-alt"
job_title_selector = ".card-head .card-head-inner h3"
job_url_selector = ".card-content .positionListButtan"

# Script input parameter: HTML file name
html_file_path = sys.argv[1]

def scrape_job_listings(html_file_path):
    profile_folder_path = f"{os.getenv("CHROME_PROFILE_PATH")}{os.path.sep}{threading.get_ident()}"

    # Create the profile directory if it does not exist
    os.makedirs(profile_folder_path, exist_ok=True)

    options = webdriver.ChromeOptions()
    options.add_argument(f"user-data-dir={profile_folder_path}")
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")

    service = Service(executable_path=r""+os.getenv("CHROME_DRIVER_PATH")+"")
    driver = webdriver.Chrome(service=service, options=options)

    # Navigate to the local HTML file
    driver.get(f"file:///{html_file_path}")

    job_listings = []
    job_elements = driver.find_elements(By.CSS_SELECTOR, job_block_selector)
    for job_element in job_elements:
        title_element = job_element.find_element(By.CSS_SELECTOR, job_title_selector)
        url_element = job_element.find_element(By.CSS_SELECTOR, job_url_selector)
        job_listings.append({
            "Job-title": title_element.text.strip(),
            "URL": url_element.get_attribute("href").strip(),
        })

    driver.quit()

    # Remove the profile directory
    # shutil.rmtree(profile_folder_path, ignore_errors=True)

    return json.dumps(job_listings)

# Execute and print the result
if __name__ == "__main__":
    print(scrape_job_listings(html_file_path))
