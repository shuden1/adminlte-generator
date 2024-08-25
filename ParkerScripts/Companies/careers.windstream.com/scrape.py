import sys
from selenium import webdriver
import os
from dotenv import load_dotenv

load_dotenv()
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
import shutil
import threading
import json

# Step 1: Selectors definition based on BeautifulSoup analysis (defined previously)
job_block_selector = ".job-result"
job_title_selector = ".job-result-title-cell .job-result-title"
job_url_selector = ".job-result-title-cell .job-result-title"

# Step 2: Selenium Script
def main(target_html_file):
    # Initialize webdriver options and service
    profile_folder_path = os.getenv("CHROME_PROFILE_PATH") + "\\" + str(threading.get_ident())
    service = ChromeService(executable_path=r""+os.getenv("CHROME_DRIVER_PATH")+"")
    options = webdriver.ChromeOptions()
    options.add_argument(f"user-data-dir={profile_folder_path}")
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")

    # Start headless ChromeDriver
    driver = webdriver.Chrome(service=service, options=options)

    try:
        # Open the target HTML file
        driver.get(f"file://{target_html_file}")

        # Find all job listings using defined selectors
        job_blocks = driver.find_elements(By.CSS_SELECTOR, job_block_selector)
        jobs = []

        for job_block in job_blocks:
            title_element = job_block.find_element(By.CSS_SELECTOR, job_title_selector)
            job_title = title_element.text
            job_url = title_element.get_attribute("href")

            # Append to jobs list as a dictionary
            jobs.append({"Job-title": job_title, "URL": job_url})

        # Convert job listing to JSON format
        jobs_json = json.dumps(jobs)

        # Output the JSON result
        print(jobs_json)

    finally:
        # Quit the driver and clean up the profile directory
        driver.quit()


# Read target HTML file from console argument
if __name__ == "__main__":
    target_html_file = sys.argv[1]  # This will be supplied by external source
    main(target_html_file)
