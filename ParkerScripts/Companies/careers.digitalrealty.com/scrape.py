from bs4 import BeautifulSoup
from selenium import webdriver
import os
from dotenv import load_dotenv

load_dotenv()
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
import threading, shutil, sys, json

# STEP 1: Identifying the EXACT HTML selectors
# Based on the given HTML snippet above
job_blocks_selector = ".jobs-section__item"
job_title_selector = ".job-title a"
job_url_selector = ".job-title a"  # The URL is the 'href' attribute of the 'a' tag

# Proceeding to STEP 2 with the identified selectors

# 2) Initialise a headless webdriver, with this profile path
profile_folder_path = os.getenv("CHROME_PROFILE_PATH") + "\\" + str(threading.get_ident())
service = ChromeService(executable_path=r""+os.getenv("CHROME_DRIVER_PATH")+"")
options = webdriver.ChromeOptions()
options.add_argument(f"user-data-dir={profile_folder_path}")
options.add_argument("--headless")
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")

# Launching the webdriver with the above options
driver = webdriver.Chrome(service=service, options=options)

# Get HTML file name from argument
file_name = sys.argv[1]

# Open the given HTML file
driver.get(f"file:///{file_name}")

# 3) Scrape all job listings using the defined selectors
job_blocks = driver.find_elements(by=By.CSS_SELECTOR, value=job_blocks_selector)
jobs = []

# Extract the job titles and URLs
for job_block in job_blocks:
    title_element = job_block.find_element(by=By.CSS_SELECTOR, value=job_title_selector)
    job_title = title_element.text
    job_url = title_element.get_attribute('href')
    jobs.append({"Job-title": job_title, "URL": job_url})

driver.quit()

# 5) Return a JSON in the following format
print(json.dumps(jobs))

# 6) Remove the folder profile_folder_path
