import sys
import threading
import shutil
from selenium import webdriver
import os
from dotenv import load_dotenv

load_dotenv()
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import json

# Retrieve the argument for the HTML file name
html_file_name = sys.argv[1]

# Selectors identified from Step 1
job_block_selector = ".css-1q2dra3"
job_title_selector = "h3 .css-19uc56f"

# Initialize the headless webdriver with specified options
profile_folder_path = f"{os.getenv("CHROME_PROFILE_PATH")}{os.path.sep}{threading.get_ident()}"
service = ChromeService(executable_path=r""+os.getenv("CHROME_DRIVER_PATH")+"")
options = Options()
options.add_argument(f"user-data-dir={profile_folder_path}")
options.add_argument("--headless")
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")

driver = webdriver.Chrome(service=service, options=options)

# Load the provided HTML file
driver.get(f"file://{html_file_name}")

# Scrape job listings using the selectors from Step 1
job_listings = []
jobs = driver.find_elements(by=By.CSS_SELECTOR, value=job_block_selector)
for job in jobs:
    title_element = job.find_element(by=By.CSS_SELECTOR, value=job_title_selector)
    job_title = title_element.text
    job_url = title_element.get_attribute('href')
    job_listings.append({"Job-title": job_title, "URL": job_url})

# Output scraped data as JSON
print(json.dumps(job_listings))

# Quit the driver and remove the profile folder
driver.quit()
