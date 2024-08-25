import sys
from selenium import webdriver
import os
from dotenv import load_dotenv

load_dotenv()
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
import threading
import json

# Step 1: Obtain the target HTML file name from the external source (console command)
target_html_file = sys.argv[1]

# Setting up the Chrome driver with profiles and options for headless execution
profile_folder_path = os.getenv("CHROME_PROFILE_PATH") + os.path.sep + str(threading.get_ident())

service = ChromeService(executable_path=r""+os.getenv("CHROME_DRIVER_PATH")+"")
options = webdriver.ChromeOptions()
options.add_argument(f"user-data-dir={profile_folder_path}")
options.add_argument("--headless")
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")

# Initialize the webdriver
driver = webdriver.Chrome(service=service, options=options)

# Load the target HTML file
driver.get(f"file:///{target_html_file}")

# Step 2: Use the selectors defined in Step 1
job_listings = driver.find_elements(By.CSS_SELECTOR, "a.c-io-leverco-vacancy")
jobs = []

for job in job_listings:
    title = job.find_element(By.CSS_SELECTOR, "h4.js-title").text
    url = job.get_attribute("href")
    jobs.append({"Job-title": title, "URL": url})

# Output the scraped job listings as JSON
print(json.dumps(jobs))
