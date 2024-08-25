import sys
import threading
import shutil
import json
from selenium import webdriver
import os
from dotenv import load_dotenv

load_dotenv()
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service

# The target HTML file name is an argument sent from an external source through the console command
html_file = sys.argv[1]

# Initialize a headless webdriver with a profile path
profile_folder_path = f"{os.getenv("CHROME_PROFILE_PATH")}{os.path.sep}{threading.get_ident()}"

# Set up Chrome service
service = Service(executable_path=r""+os.getenv("CHROME_DRIVER_PATH")+"")

# Set up Chrome options
options = webdriver.ChromeOptions()
options.add_argument(f"user-data-dir={profile_folder_path}")
options.add_argument("--headless")
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")

# Initialize the WebDriver
driver = webdriver.Chrome(service=service, options=options)

# Open the HTML file
driver.get('file://' + html_file)

# Define selectors based on the observed structure of the job listings
job_blocks_selector = ".job_listings .job_listing"
job_title_selector = ".h5.mb-1 > a" # Fixed selector for job titles and URLs

# Scrape job listings
try:
    job_blocks = driver.find_elements(By.CSS_SELECTOR, job_blocks_selector)
    jobs_data = []

    for job_block in job_blocks:
        job_title_element = job_block.find_element(By.CSS_SELECTOR, job_title_selector)
        job_title = job_title_element.text.strip()
        job_url = job_title_element.get_attribute("href").strip()
        jobs_data.append({"Job-title": job_title, "URL": job_url})

    # Return the data as JSON
    json_data = json.dumps(jobs_data)
    print(json_data)

finally:
    driver.quit()
    # Ensure the profile directory is removed successfully
    # shutil.rmtree(profile_folder_path, ignore_errors=True)
