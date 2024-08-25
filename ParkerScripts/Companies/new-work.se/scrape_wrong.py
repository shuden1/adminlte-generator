import sys
from selenium import webdriver
import os
from dotenv import load_dotenv

load_dotenv()
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
import threading
import json

def scrape_job_listings(html_file_name):
    job_listings = []

    profile_folder_path = os.getenv("CHROME_PROFILE_PATH") + os.path.sep + str(threading.get_ident())
    service = ChromeService(executable_path=r""+os.getenv("CHROME_DRIVER_PATH")+"")
    options = webdriver.ChromeOptions()
    options.add_argument(f"user-data-dir={profile_folder_path}")
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")

    with webdriver.Chrome(service=service, options=options) as driver:
        driver.get(f"file:///{html_file_name}")

        # Since the content of the actual job listings are not visible in the provided text
        # This is a placeholder, you need to replace the 'your-job-listing-class'
        # and 'your-title-and-url-class' with the actual selectors identified in the provided HTML
        job_blocks = driver.find_elements(By.CSS_SELECTOR, "your-job-listing-class")
        for job in job_blocks:
            title_element = job.find_element(By.CSS_SELECTOR, "your-title-and-url-class")
            url = title_element.get_attribute('href')
            title = title_element.text
            job_listings.append({"Job-title": title, "URL": url})

    return json.dumps(job_listings)

if __name__ == "__main__":
    html_file_name = sys.argv[1]
    print(scrape_job_listings(html_file_name))
