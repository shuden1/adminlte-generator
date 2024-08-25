import sys
from selenium import webdriver
import os
from dotenv import load_dotenv

load_dotenv()
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
import threading
import json

# The target HTML file name is taken from the console command as a single input parameter
target_html_file = sys.argv[1]

# Setting up the Chrome driver with necessary options
service = ChromeService(executable_path=r""+os.getenv("CHROME_DRIVER_PATH")+"")
profile_folder_path = os.getenv("CHROME_PROFILE_PATH") + "\\" + str(threading.get_ident())
options = webdriver.ChromeOptions()
options.add_argument(f"user-data-dir={profile_folder_path}")
options.add_argument("--headless")
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")

# Initiating the browser
driver = webdriver.Chrome(service=service, options=options)

# Opening the target HTML file
driver.get("file:///" + target_html_file)

# Selectors identified in STEP 1
job_block_selector = ".Offers_offers__vpylO"
job_title_and_url_selector = ".Offers_offers__vpylO li a"

# Scraping job listings
job_elements = driver.find_elements(By.CSS_SELECTOR, job_title_and_url_selector)
jobs_list = []

for job_element in job_elements:
    job_title = job_element.text
    job_url = job_element.get_attribute("href")
    jobs_list.append({"Job-title": job_title, "URL": job_url})

# Outputting the scraped data as JSON
print(json.dumps(jobs_list))
