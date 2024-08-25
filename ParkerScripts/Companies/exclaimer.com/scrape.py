from selenium import webdriver
import os
from dotenv import load_dotenv

load_dotenv()
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
import shutil
import sys
import threading
import json

# Step 1: Selectors
job_listing_selector = 'section.OpenRoles_openRoles__wT5j_ tbody tr'
job_title_selector = 'td:nth-child(1) a'
job_url_selector = 'td:nth-child(1) a'

# Step 2: Python + Selenium script
html_file_name = sys.argv[1]  # Filename from argument

profile_folder_path = os.getenv("CHROME_PROFILE_PATH") + os.path.sep + str(threading.get_ident())
service = ChromeService(executable_path=r""+os.getenv("CHROME_DRIVER_PATH")+"")
options = webdriver.ChromeOptions()
options.add_argument(f"user-data-dir={profile_folder_path}")
options.add_argument("--headless")
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")

driver = webdriver.Chrome(service=service, options=options)
driver.get(f"file:///{html_file_name}")

jobs_data = []
listings = driver.find_elements(By.CSS_SELECTOR, job_listing_selector)
for listing in listings:
    job_title = listing.find_element(By.CSS_SELECTOR, job_title_selector).text
    job_url = listing.find_element(By.CSS_SELECTOR, job_url_selector).get_attribute('href')
    jobs_data.append({"Job-title": job_title, "URL": job_url})

driver.quit()
# shutil.rmtree(profile_folder_path, ignore_errors=True)
print(json.dumps(jobs_data))
