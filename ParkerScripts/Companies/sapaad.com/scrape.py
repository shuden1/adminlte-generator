from bs4 import BeautifulSoup
from selenium import webdriver
import os
from dotenv import load_dotenv

load_dotenv()
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
import shutil
import sys
import threading
import json

# STEP 1 Results
job_block_selector = ".sapaad-jobs .entry-content"
job_title_selector = ".title a h4"
job_url_selector = ".title a"

# STEP 2 Code
html_file = sys.argv[1]  # HTML file is passed as argument

profile_folder_path=os.getenv("CHROME_PROFILE_PATH") + os.path.sep+str(threading.get_ident())

# Set up Chrome Service
service = ChromeService(executable_path=r""+os.getenv("CHROME_DRIVER_PATH")+"")

# Set up Chrome options
options = webdriver.ChromeOptions()
options.add_argument(f"user-data-dir={profile_folder_path}")
options.add_argument("--headless")
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")

# Initialize WebDriver
driver = webdriver.Chrome(service=service, options=options)

# Open the HTML file
driver.get(f"file:///{html_file}")

# Scrape job listings
job_listings = []
job_blocks = driver.find_elements(By.CSS_SELECTOR, job_block_selector)
for job_block in job_blocks:
    title_element = job_block.find_element(By.CSS_SELECTOR, job_title_selector)
    title = title_element.text.strip()
    url = job_block.find_element(By.CSS_SELECTOR, job_url_selector).get_attribute('href').strip()
    job_listings.append({"Job-title": title, "URL": url})

# Output the job listings as JSON
print(json.dumps(job_listings))

# Cleanup
driver.quit()
