import sys
from selenium import webdriver
import os
from dotenv import load_dotenv

load_dotenv()
from selenium.webdriver.chrome.service import Service as service
from selenium.webdriver.common.by import By
import threading
import json

# Retrieve the target HTML file name from command line arguments
target_html_file = sys.argv[1]

# WebDriver setup and options
profile_folder_path = os.getenv("CHROME_PROFILE_PATH") + "\\" + str(threading.get_ident())
options = webdriver.ChromeOptions()
options.add_argument(f"user-data-dir={profile_folder_path}")
options.add_argument("--headless")
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")
service = service(executable_path=r""+os.getenv("CHROME_DRIVER_PATH")+"")

# Initialize WebDriver
driver = webdriver.Chrome(service=service, options=options)

# Open the target HTML file
driver.get(f"file:///{target_html_file}")

# Find job listings using defined selectors from Step 1
job_listings = driver.find_elements(By.CSS_SELECTOR, ".data-row .colTitle .jobTitle .jobTitle-link")

# Extract job titles and URLs
jobs = []
for listing in job_listings:
    job_title = listing.text
    job_url = listing.get_attribute('href')
    jobs.append({"Job-title": job_title, "URL": job_url})

driver.quit()

# Convert jobs list to JSON format and print
print(json.dumps(jobs))
