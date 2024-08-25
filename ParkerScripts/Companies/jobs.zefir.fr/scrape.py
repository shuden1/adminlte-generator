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
    # Profile folder path
    profile_folder_path = f"{os.getenv("CHROME_PROFILE_PATH")}{os.path.sep}{str(threading.get_ident())}"

    # Chrome options
    options = Options()
    options.add_argument(f"user-data-dir={profile_folder_path}")
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")

    # Chrome service
    service = Service(executable_path=r""+os.getenv("CHROME_DRIVER_PATH")+"")

    # Initialize WebDriver
    driver = webdriver.Chrome(service=service, options=options)

    # Open the HTML file
    driver.get(f"file:///{file_path}")

    # Selectors
    job_block_selector = 'div[data-job-list-items]'
    job_title_selector = 'p.JobListItems__jobTitle__6cPrj'
    job_url_selector = 'a.JobListItems__lightListItem__Ev5JI'

    # Scrape job listings
    job_openings = []
    job_blocks = driver.find_elements(By.CSS_SELECTOR, job_block_selector)
    for job_block in job_blocks:
        job_elements = job_block.find_elements(By.CSS_SELECTOR, job_url_selector)
        for job_element in job_elements:
            job_title = job_element.find_element(By.CSS_SELECTOR, job_title_selector).text
            job_url = job_element.get_attribute('href')
            job_openings.append({"Job-title": job_title, "URL": job_url})

    # Close the WebDriver
    driver.quit()

    # Return job listings as JSON
    return json.dumps(job_openings, indent=4)

if __name__ == "__main__":
    file_path = sys.argv[1]
    job_listings_json = scrape_jobs(file_path)
    print(job_listings_json)
