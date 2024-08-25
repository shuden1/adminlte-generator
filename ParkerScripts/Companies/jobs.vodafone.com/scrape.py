from selenium import webdriver
import os
from dotenv import load_dotenv

load_dotenv()
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import shutil
import threading
import json
import sys

# Define selectors
job_block_selector = ".card.position-card.pointer"
title_selector = ".position-title.line-clamp"

# Target HTML file name passed as an argument from the console command
target_html_file = sys.argv[1]

# Initialise headless webdriver
profile_folder_path = os.getenv("CHROME_PROFILE_PATH") + "\\" + str(threading.get_ident())
service = Service(executable_path=r""+os.getenv("CHROME_DRIVER_PATH")+"")
options = Options()
options.add_argument(f"user-data-dir={profile_folder_path}")
options.add_argument("--headless")
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")

# Start webdriver
driver = webdriver.Chrome(service=service, options=options)
driver.get(f"file:///{target_html_file}")

# Scrape job listings
jobs = []
job_elements = driver.find_elements(By.CSS_SELECTOR, job_block_selector)
for job_element in job_elements:
    title_element = job_element.find_element(By.CSS_SELECTOR, title_selector)
    job_title = title_element.text.strip()
    job_url = job_element.get_attribute('onclick').split("'")[1] if job_element.get_attribute('onclick') else ""

    jobs.append({"Job-title": job_title, "URL": job_url})

# Return JSON
print(json.dumps(jobs))

# Cleanup
driver.quit()
# shutil.rmtree(profile_folder_path, ignore_errors=True)
