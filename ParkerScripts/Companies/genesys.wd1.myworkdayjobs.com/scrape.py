from selenium import webdriver
import os
from dotenv import load_dotenv

load_dotenv()
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
import shutil
import json
import sys
import threading

def scrape_job_listings(html_file):
    service = Service(executable_path=r""+os.getenv("CHROME_DRIVER_PATH")+"")
    profile_folder_path = os.getenv("CHROME_PROFILE_PATH") + os.path.sep + str(threading.get_ident())
    options = webdriver.ChromeOptions()
    options.add_argument(f"user-data-dir={profile_folder_path}")
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")

    with webdriver.Chrome(service=service, options=options) as driver:
        driver.get(f"file://{html_file}")
        job_elements = driver.find_elements(By.CSS_SELECTOR, 'h3 a.css-19uc56f')
        job_listings = []

        for job_element in job_elements:
            job_title = job_element.text
            job_url = job_element.get_attribute('href')
            job_listings.append({"Job-title": job_title, "URL": job_url})

        # Returning the JSON representation of job listings
        return json.dumps(job_listings)

    # Cleanup the profile directory at the end of the script


if __name__ == "__main__":
    html_file_name = sys.argv[1]  # Expected to be the path to the HTML file
    print(scrape_job_listings(html_file_name))
