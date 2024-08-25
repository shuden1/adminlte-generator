import sys
from selenium import webdriver
import os
from dotenv import load_dotenv

load_dotenv()
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
import threading
import shutil
import json

# Extract the target HTML file name from the command line argument
target_html_file = sys.argv[1]

# Initialise a headless Chrome webdriver
profile_folder_path = os.getenv("CHROME_PROFILE_PATH") + os.path.sep + str(threading.get_ident())
service = ChromeService(executable_path=r""+os.getenv("CHROME_DRIVER_PATH")+"")
options = webdriver.ChromeOptions()
options.add_argument(f"user-data-dir={profile_folder_path}")
options.add_argument("--headless")
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")
driver = webdriver.Chrome(service=service, options=options)

# Open the target HTML file
driver.get(f"file:///{target_html_file}")

# Scrape all job listings
job_selector = ".posTitle.reqitem.ReqRowClick"
title_selector = "a"
jobs = driver.find_elements(By.CSS_SELECTOR, job_selector)
job_data = []
for job in jobs:
    title_element = job.find_element(By.CSS_SELECTOR, title_selector)
    job_title = title_element.text.strip()
    job_url = title_element.get_attribute('href')
    job_data.append({"Job-title": job_title, "URL": job_url})

# Convert job data to JSON format
job_json = json.dumps(job_data)

# Output the JSON
print(job_json)

# Clean up by removing the user profile directory


# Exit the webdriver
driver.quit()
