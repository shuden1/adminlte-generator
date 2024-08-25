import sys
from selenium import webdriver
import os
from dotenv import load_dotenv

load_dotenv()
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
import threading
import json

# Get HTML file name from external argument
html_file_name = sys.argv[1]

# Initialize WebDriver
profile_folder_path = os.getenv("CHROME_PROFILE_PATH") + "\\" + str(threading.get_ident())
service = ChromeService(executable_path=r""+os.getenv("CHROME_DRIVER_PATH")+"")
options = webdriver.ChromeOptions()
options.add_argument(f"user-data-dir={profile_folder_path}")
options.add_argument("--headless")
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")
driver = webdriver.Chrome(service=service, options=options)

# Open the local HTML file
driver.get(f"file:///{html_file_name}")

# Get job listings
job_listings = driver.find_elements(By.CSS_SELECTOR, "div.job-listing a")

# Extract job titles and URLs
jobs = []
for listing in job_listings:
    job_title = listing.text
    job_url = listing.get_attribute('href')
    jobs.append({"Job-title": job_title, "URL": job_url})

# Convert jobs list to JSON
jobs_json = json.dumps(jobs)

# Output the JSON
print(jobs_json)

# Quit the driver
driver.quit()
