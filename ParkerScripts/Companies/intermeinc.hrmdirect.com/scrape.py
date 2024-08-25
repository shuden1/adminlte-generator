import threading
import shutil
from selenium import webdriver
import os
from dotenv import load_dotenv

load_dotenv()
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
import json
import sys

# STEP 1 results
job_block_selector = 'tr[class^="reqitem"]'
job_title_selector = 'td.posTitle a'
job_url_attribute = 'href'

# STEP 2
html_file_name = sys.argv[1]

# Webdriver configuration
profile_folder_path = os.getenv("CHROME_PROFILE_PATH") + os.path.sep + str(threading.get_ident())
service = ChromeService(executable_path=r""+os.getenv("CHROME_DRIVER_PATH")+"")
options = webdriver.ChromeOptions()
options.add_argument(f"user-data-dir={profile_folder_path}")
options.add_argument("--headless")
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")

# Start webdriver
driver = webdriver.Chrome(service=service, options=options)

# Open the target HTML file
driver.get(f"file:///{html_file_name}")

# Scrape job listings
job_listings = []
for job_element in driver.find_elements(By.CSS_SELECTOR, job_block_selector):
    job_title_element = job_element.find_element(By.CSS_SELECTOR, job_title_selector)
    job_title = job_title_element.text
    job_url = job_title_element.get_attribute(job_url_attribute)
    job_listings.append({"Job-title": job_title, "URL": job_url})

# Return results as JSON
print(json.dumps(job_listings))

# Clean up
driver.quit()
