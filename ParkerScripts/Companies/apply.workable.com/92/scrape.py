import sys
from selenium import webdriver
import os
from dotenv import load_dotenv

load_dotenv()
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
import threading
import json

# Extract the target HTML file name from the command line argument
filename = sys.argv[1]

# Setup Selenium Webdriver with options
profile_folder_path = os.getenv("CHROME_PROFILE_PATH") + os.path.sep + str(threading.get_ident())
service = ChromeService(executable_path=r""+os.getenv("CHROME_DRIVER_PATH")+"")
options = webdriver.ChromeOptions()
options.add_argument(f"user-data-dir={profile_folder_path}")
options.add_argument("--headless")
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")

# Start the headless browser
driver = webdriver.Chrome(service=service, options=options)

# Open the given HTML file in the browser
driver.get(f"file:///{filename}")

# Extract job titles and URLs using the new selectors
job_selector = ".styles--1vo9F"  # Selector for job listing blocks
title_selector = ".styles--3TJHk"  # Selector for job titles
url_selector = ".styles--1OnOt"  # Updated selector to match <a> tags where URLs are expected to be

# Find all job listing blocks
job_blocks = driver.find_elements(By.CSS_SELECTOR, job_selector)
job_listings = []

# Iterate through all job listing blocks and extract the title and URL
for job_block in job_blocks:
    job_title_element = job_block.find_element(By.CSS_SELECTOR, title_selector)
    job_title = job_title_element.text.strip()

    job_url_elements = job_block.find_elements(By.CSS_SELECTOR, url_selector)
    job_url = job_url_elements[0].get_attribute('href') if job_url_elements else None

    job_listings.append({"Job-title": job_title, "URL": job_url})

# Return the extracted data in JSON format
print(json.dumps(job_listings))

# Close the browser
driver.quit()
