import sys
from selenium import webdriver
import os
from dotenv import load_dotenv

load_dotenv()
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import threading
import shutil
import json

# The target HTML file name, as an argument from the external source
html_file_name = sys.argv[1]

profile_folder_path=os.getenv("CHROME_PROFILE_PATH") + "\\"+str(threading.get_ident())

# Setting up Chrome options for headless browsing
options = webdriver.ChromeOptions()
options.add_argument(f"user-data-dir={profile_folder_path}")
options.add_argument("--headless")
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")

# Set up Selenium WebDriver
service=Service(executable_path=r""+os.getenv("CHROME_DRIVER_PATH")+"")
driver = webdriver.Chrome(service=service, options=options)

# Open the HTML file
driver.get(f"file:///{html_file_name}")

# Selectors from STEP 1
job_blocks_selector = ".article.article--result"
job_title_selector = "h3.article__header__text__title--4 a"

# Find all job listing elements
job_elements = driver.find_elements(By.CSS_SELECTOR, job_blocks_selector)

# Scrape job titles and urls
jobs = []
for job_element in job_elements:
    title_element = job_element.find_element(By.CSS_SELECTOR, job_title_selector)
    job_title = title_element.text.strip()
    job_url = title_element.get_attribute('href')
    jobs.append({"Job-title": job_title, "URL": job_url})

# Convert to JSON format
jobs_json = json.dumps(jobs, ensure_ascii=False)

# Writing to stdout (console) in a way that avoids UnicodeEncodeError
sys.stdout.buffer.write(jobs_json.encode('utf8'))

# Quit the driver
driver.quit()

# Remove the profile folder
