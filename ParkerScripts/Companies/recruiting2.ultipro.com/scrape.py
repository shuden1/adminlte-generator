import sys
import json
from selenium import webdriver
import os
from dotenv import load_dotenv

load_dotenv()
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
import shutil
import threading

# Receive the target HTML file name from the console command
target_html_file = sys.argv[1]

# Initialise a headless webdriver with profile path
profile_folder_path = os.getenv("CHROME_PROFILE_PATH") + "\\" + str(threading.get_ident())
options = webdriver.ChromeOptions()
options.add_argument(f"user-data-dir={profile_folder_path}")
options.add_argument("--headless")
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")
service = ChromeService(executable_path=r""+os.getenv("CHROME_DRIVER_PATH")+"")

# Start driver
driver = webdriver.Chrome(service=service, options=options)

# Open the local HTML file
driver.get(f"file:///{target_html_file}")

# Scrape job listings using selectors defined in STEP 1
job_blocks_selector = '.opportunity'
job_title_selector = '.opportunity-link.break-word'
job_listings = []

for job_block in driver.find_elements(By.CSS_SELECTOR, job_blocks_selector):
    title_element = job_block.find_element(By.CSS_SELECTOR, job_title_selector)
    job_title = title_element.text
    job_url = title_element.get_attribute('href')
    job_listings.append({"Job-title": job_title, "URL": job_url})

# Return JSON
print(json.dumps(job_listings, ensure_ascii=False))

# Clean up
driver.quit()
