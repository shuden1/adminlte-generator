import sys
from selenium import webdriver
import os
from dotenv import load_dotenv

load_dotenv()
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
import threading
import json

# Capturing the filename from the console command
html_file = sys.argv[1]

# Setting up browser profile
profile_folder_path = os.getenv("CHROME_PROFILE_PATH") + "\\" + str(threading.get_ident())

service = ChromeService(executable_path=r""+os.getenv("CHROME_DRIVER_PATH")+"")
options = webdriver.ChromeOptions()
options.add_argument(f"user-data-dir={profile_folder_path}")
options.add_argument("--headless")
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")

# Initializing WebDriver
driver = webdriver.Chrome(service=service, options=options)

# Opening the HTML file
driver.get(f"file:///{html_file}")

# Using selectors defined in Step 1
job_openings_selector = ".job-offers__list .job-preview"
job_title_and_url_selector = ".job-preview__header a"

jobs = []
job_elements = driver.find_elements(By.CSS_SELECTOR, job_openings_selector)
for job in job_elements:
    title_element = job.find_element(By.CSS_SELECTOR, job_title_and_url_selector)
    job_title = title_element.text
    job_url = title_element.get_attribute('href')
    jobs.append({"Job-title": job_title, "URL": job_url})

# Outputting the job listings in JSON format
print(json.dumps(jobs))

driver.quit()
