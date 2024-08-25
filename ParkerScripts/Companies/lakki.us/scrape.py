import sys
from selenium import webdriver
import os
from dotenv import load_dotenv

load_dotenv()
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
import threading
import json

# Read command line argument for filename
filename = sys.argv[1]

# Set up ChromeDriver options and profile
profile_folder_path = os.getenv("CHROME_PROFILE_PATH") + "\\"+str(threading.get_ident())
service = ChromeService(executable_path=r""+os.getenv("CHROME_DRIVER_PATH")+"")
options = webdriver.ChromeOptions()
options.add_argument(f"user-data-dir={profile_folder_path}")
options.add_argument("--headless")
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")

# Initialize WebDriver
driver = webdriver.Chrome(service=service, options=options)

# Load the HTML file
driver.get(f"file:///{filename}")

# Define selectors for job openings
job_listing_selector = "tr:not(:first-child)"  # Jobs are listed within <tr> elements excluding the header row.
title_selector = "td a"  # Job titles are within <a> tags inside <td> elements.

# Scrape job listings
jobs = []
for job_element in driver.find_elements(By.CSS_SELECTOR, job_listing_selector):
    title_element = job_element.find_element(By.CSS_SELECTOR, title_selector)  # Assuming there's only one <a> per job listing.
    job = {
        "Job-title": title_element.text,
        "URL": title_element.get_attribute('href')
    }
    jobs.append(job)

# Close the WebDriver
driver.quit()

# Print jobs in JSON format
print(json.dumps(jobs, indent=2))
