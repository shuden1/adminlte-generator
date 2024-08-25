import sys
from selenium import webdriver
import os
from dotenv import load_dotenv

load_dotenv()
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
import threading
import json

# STEP 1: Extracted selectors from the HTML analysis
job_block_selector = ".ds-jobs-card-wrapper .ds-jobs-card"
job_title_selector = ".job-card-title"
job_url_selector = "not directly available in the provided HTML snippet"

# STEP 2: Python + Selenium script as per the instructions

# The target HTML file name is provided as a command line argument
file_name = sys.argv[1]

profile_folder_path = os.getenv("CHROME_PROFILE_PATH") + "\\" + str(threading.get_ident())

# Initialize chrome options
options = webdriver.ChromeOptions()
options.add_argument(f"user-data-dir={profile_folder_path}")
options.add_argument("--headless")
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")

# Set up service
service = ChromeService(executable_path=r""+os.getenv("CHROME_DRIVER_PATH")+"")

# Initialize the webdriver with the service and options specified
driver = webdriver.Chrome(service=service, options=options)

# Open the HTML file
driver.get(f"file:///{file_name}")

# Initialize an empty list to hold the job details
jobs = []

# Find the job listing elements
job_elements = driver.find_elements(By.CSS_SELECTOR, job_block_selector)

for job_element in job_elements:
    # Extract job title
    job_title = job_element.find_element(By.CSS_SELECTOR, job_title_selector).text
    # The job URL cannot be extracted directly from the provided information
    # Hence, we'll not include it in the output
    # Assuming job_url would be extracted here if it was possible
    jobs.append({"Job-title": job_title, "URL": "URL not available"})

# Convert the list of jobs to JSON format
jobs_json = json.dumps(jobs)

# Close the webdriver
driver.quit()

# Print the jobs in JSON format
print(jobs_json)
