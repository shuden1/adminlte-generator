import sys
import threading
import shutil
from selenium import webdriver
import os
from dotenv import load_dotenv

load_dotenv()
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
import json

# STEP 2: Selenium Script
html_file_name = sys.argv[1]  # HTML file name received as an argument from an external source

# Initialize WebDriver with headless option
profile_folder_path = os.getenv("CHROME_PROFILE_PATH") + os.path.sep + str(threading.get_ident())
service = ChromeService(executable_path=r""+os.getenv("CHROME_DRIVER_PATH")+"")
options = webdriver.ChromeOptions()
options.add_argument(f"user-data-dir={profile_folder_path}")
options.add_argument("--headless")
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")
driver = webdriver.Chrome(service=service, options=options)

# Open the HTML file
driver.get(f"file://{html_file_name}")

# Using the selectors from STEP 1 to find the Job Title and URLs
job_blocks_selector = "section#vacancies > div.container > div.row > div > article"
job_title_selector = "a.post-title"
jobs = []

for job_block in driver.find_elements(By.CSS_SELECTOR, job_blocks_selector):
    title_element = job_block.find_element(By.CSS_SELECTOR, job_title_selector)
    job_title = title_element.text
    job_url = title_element.get_attribute("href")
    jobs.append({"Job-title": job_title, "URL": job_url})

# Return a JSON
print(json.dumps(jobs))

# Cleanup: close the driver and remove profile folder
driver.quit()
