import sys
from selenium import webdriver
import os
from dotenv import load_dotenv

load_dotenv()
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
import threading
import os
import json
import shutil

# Get HTML file name from the command line argument
html_file_name = sys.argv[1]

# Set up Chrome options for headless browsing
options = webdriver.ChromeOptions()
profile_folder_path = f"D:\\Mind\\CRA\\AI_Experiments\\Job_Crawlers\\Peter\\adminlte-generator\\chrome_profile\\{threading.get_ident()}"
options.add_argument(f"user-data-dir={profile_folder_path}")
options.add_argument("--headless")
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")

# Set up Chrome service
service = ChromeService(executable_path=r""+os.getenv("CHROME_DRIVER_PATH")+"")

# Initialize the Chrome driver
driver = webdriver.Chrome(service=service, options=options)

# Open the local HTML file
driver.get(f"file:///{html_file_name}")

# Selectors defined from the provided HTML content
job_block_selector = "li.prod-flex"
job_link_selector = "a.job-link"
job_title_selector = "span.job-title"

# Scrape job listings
jobs = []
elements = driver.find_elements(By.CSS_SELECTOR, job_block_selector)
for element in elements:
    job_link_element = element.find_element(By.CSS_SELECTOR, job_link_selector)
    job_title_element = job_link_element.find_element(By.CSS_SELECTOR, job_title_selector)
    job_title = job_title_element.text
    job_url = job_link_element.get_attribute('href')
    jobs.append({"Job-title": job_title, "URL": job_url})

# Output the results as JSON
print(json.dumps(jobs))

# Clean up: close the driver and remove the profile folder
driver.quit()
