import sys
import json
import threading
from selenium import webdriver
import os
from dotenv import load_dotenv

load_dotenv()
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

def scrape_jobs(file_name):
    # Initialize Chrome options
    profile_folder_path = os.getenv("CHROME_PROFILE_PATH") + os.path.sep + str(threading.get_ident())
    options = Options()
    options.add_argument(f"user-data-dir={profile_folder_path}")
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")

    # Initialize Chrome service
    service = Service(executable_path=r""+os.getenv("CHROME_DRIVER_PATH")+"")

    # Initialize WebDriver
    driver = webdriver.Chrome(service=service, options=options)

    try:
        # Load the HTML file
        driver.get(f"file:///{file_name}")

        # Use the selectors defined in STEP 1 to find job listings
        job_opening_blocks_selector = 'a[href*="pvs=25"]'
        job_title_selector = 'a[href*="pvs=25"]'

        job_elements = driver.find_elements(By.CSS_SELECTOR, job_opening_blocks_selector)
        job_details = []

        for job_element in job_elements:
            title = job_element.text
            url = job_element.get_attribute('href')
            # Filter out non-job related titles
            if "job" in title.lower() or "manager" in title.lower() or "lead" in title.lower() or "consultant" in title.lower():
                job_details.append({"Job-title": title, "URL": url})

        # Return the job details as JSON
        print(json.dumps(job_details, indent=4))

    finally:
        driver.quit()

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script.py <html_file_path>")
        sys.exit(1)

    file_name = sys.argv[1]
    scrape_jobs(file_name)
