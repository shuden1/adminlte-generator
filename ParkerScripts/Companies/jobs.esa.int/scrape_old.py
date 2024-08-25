from selenium import webdriver
import os
from dotenv import load_dotenv

load_dotenv()
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
import threading
import sys
import json

# Target HTML file name received as an argument from the external source
target_html_file = sys.argv[1]

# Initialising a headless webdriver
profile_folder_path = os.getenv("CHROME_PROFILE_PATH") + "\\" + str(threading.get_ident())
service = ChromeService(executable_path=r""+os.getenv("CHROME_DRIVER_PATH")+"")
options = webdriver.ChromeOptions()
options.add_argument(f"user-data-dir={profile_folder_path}")
options.add_argument("--headless")
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")
driver = webdriver.Chrome(service=service, options=options)

# Open the target HTML file
driver.get(f"file:///{target_html_file}")

# Scraping job listings
job_elements = driver.find_elements(By.CSS_SELECTOR, ".job-list .job-tile")
jobs = []

for job_element in job_elements:
    title_element = job_element.find_element(By.CSS_SELECTOR, ".jobTitle-link")
    job_title = title_element.text.strip()
    job_url = title_element.get_attribute('href')
    jobs.append({"Job-title": job_title, "URL": job_url})

# Convert the job list to JSON format
jobs_json = json.dumps(jobs)

# Output the JSON, no writing to file
print(jobs_json)

# Ensure the driver is quit properly
driver.quit()
