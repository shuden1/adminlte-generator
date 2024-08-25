from selenium import webdriver
import os
from dotenv import load_dotenv

load_dotenv()
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
import json
import shutil
import sys
import threading

# STEP 1 Results:
# Exact selectors representing the blocks with Job Openings
job_block_selector = "div.result"
# Exact selectors for job titles and associated URLs
job_title_selector = ".card-header"
job_url_selector = ".btn-more-info"

# STEP 2:
if __name__ == "__main__":
    # Target HTML file as an argument from the console command
    target_html_file = sys.argv[1]

    # Initialize a headless webdriver using Chrome
    service = ChromeService(executable_path=r""+os.getenv("CHROME_DRIVER_PATH")+"")
    profile_folder_path = f"{os.getenv("CHROME_PROFILE_PATH")}{os.path.sep}{threading.get_ident()}"
    options = webdriver.ChromeOptions()
    options.add_argument(f"user-data-dir={profile_folder_path}")
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    driver = webdriver.Chrome(service=service, options=options)

    # Open the target HTML file
    driver.get(f"file://{target_html_file}")

    # Scrape job listings
    jobs_data = []
    job_elements = driver.find_elements(By.CSS_SELECTOR, job_block_selector)
    for job_element in job_elements:
        job_title_element = job_element.find_element(By.CSS_SELECTOR, job_title_selector)
        job_url_element = job_element.find_element(By.CSS_SELECTOR, job_url_selector)
        jobs_data.append({"Job-title": job_title_element.text, "URL": job_url_element.get_attribute("href")})

    # Output jobs data as JSON
    print(json.dumps(jobs_data))

    # Close browser
    driver.quit()

    # Remove profile folder
