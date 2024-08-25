from selenium import webdriver
import os
from dotenv import load_dotenv

load_dotenv()
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import threading
import shutil
import json
import sys

# Step 1
job_blocks_selector = ".jobs-container .w-dyn-item"
job_title_selector = ".jobs-title-text-block"
job_url_selector = "a"

# Retrieve the HTML file name from the command line argument
file_name = sys.argv[1]

profile_folder_path = f"{os.getenv("CHROME_PROFILE_PATH")}{os.path.sep}{threading.get_ident()}"
service = Service(executable_path=r""+os.getenv("CHROME_DRIVER_PATH")+"")

options = webdriver.ChromeOptions()
options.add_argument(f"user-data-dir={profile_folder_path}")
options.add_argument("--headless")

# Initialize driver with options
driver = webdriver.Chrome(service=service, options=options)
driver.get(f"file://{file_name}")

# Scrape job listings
job_elements = driver.find_elements(By.CSS_SELECTOR, job_blocks_selector)
jobs = [{"Job-title": job_element.find_element(By.CSS_SELECTOR, job_title_selector).text,
         "URL": job_element.find_element(By.CSS_SELECTOR, job_url_selector).get_attribute('href')}
         for job_element in job_elements]

driver.quit()

# Remove the user profile directory for the current thread


# Output scraped job listings in JSON format
print(json.dumps(jobs))
