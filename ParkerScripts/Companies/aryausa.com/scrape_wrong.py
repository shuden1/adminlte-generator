import sys
from selenium import webdriver
import os
from dotenv import load_dotenv

load_dotenv()
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
import threading
import json

# Extract the target HTML file name from the console command
target_html_file_name = sys.argv[1]

# Setup Chrome WebDriver
profile_folder_path = os.getenv("CHROME_PROFILE_PATH") + os.path.sep + str(threading.get_ident())
service = ChromeService(executable_path=r""+os.getenv("CHROME_DRIVER_PATH")+"")
options = webdriver.ChromeOptions()
options.add_argument(f"user-data-dir={profile_folder_path}")
options.add_argument("--headless")
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")

driver = webdriver.Chrome(service=service, options=options)

# Open the HTML file
driver.get(f"file:///{target_html_file_name}")

# Scrape job listings
job_elements = driver.find_elements(By.CSS_SELECTOR, ".job-listing .job-link")
jobs_output = []

for job_element in job_elements:
    job_title = job_element.text
    job_url = job_element.get_attribute('href')
    jobs_output.append({"Job-title": job_title, "URL": job_url})

driver.quit()

# Print the results in JSON format
print(json.dumps(jobs_output))
