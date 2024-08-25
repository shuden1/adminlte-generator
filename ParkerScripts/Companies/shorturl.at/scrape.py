from bs4 import BeautifulSoup
import json
import os
import shutil
import sys
import threading
from selenium import webdriver
import os
from dotenv import load_dotenv

load_dotenv()
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By

# Step 1 Results
job_listing_selector = ".card.card-job"
job_title_selector = ".card-title a"
job_url_selector = ".card-title a"

# Step 2 Script

# Get target HTML file name from console argument
target_html_file_name = sys.argv[1]

# Initialize headless webdriver with profile
profile_folder_path = os.getenv("CHROME_PROFILE_PATH") + "\\" + str(threading.get_ident())

# Setting service
service = ChromeService(executable_path=r""+os.getenv("CHROME_DRIVER_PATH")+"")
options = webdriver.ChromeOptions()
options.add_argument(f"user-data-dir={profile_folder_path}")
options.add_argument("--headless")
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")
driver = webdriver.Chrome(service=service, options=options)

# Load the page from the filesystem
driver.get(f"file://{os.path.abspath(target_html_file_name)}")

# Scrape job listings
jobs = []
job_elements = driver.find_elements(By.CSS_SELECTOR, job_listing_selector)
for job_element in job_elements:
    title_element = job_element.find_element(By.CSS_SELECTOR, job_title_selector)
    job_title = title_element.text
    job_url = title_element.get_attribute('href')
    jobs.append({"Job-title": job_title, "URL": job_url})

# Print results as JSON
print(json.dumps(jobs))

# Quit the driver and remove the profile folder
driver.quit()
