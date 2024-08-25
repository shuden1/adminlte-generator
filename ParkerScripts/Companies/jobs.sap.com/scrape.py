import sys
from selenium import webdriver
import os
from dotenv import load_dotenv

load_dotenv()
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
import threading
import json

# The target HTML file name is received from an external source through the console command as the single input parameter.
target_html_file = sys.argv[1]

# Initialise a headless webdriver
profile_folder_path = os.getenv("CHROME_PROFILE_PATH") + "\\" + str(threading.get_ident())
service = ChromeService(executable_path=r""+os.getenv("CHROME_DRIVER_PATH")+"")
options = webdriver.ChromeOptions()
options.add_argument(f"user-data-dir={profile_folder_path}")
options.add_argument("--headless")
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")

driver = webdriver.Chrome(service=service, options=options)

# Open the provided HTML file
driver.get(f"file:///{target_html_file}")

# Use the defined selectors from STEP 1 to scrape all job listings
job_elements = driver.find_elements(By.CSS_SELECTOR, "table.searchResults.full.table.table-striped.table-hover tbody tr.data-row")
jobs = []

for element in job_elements:
    job_title_element = element.find_element(By.CSS_SELECTOR, "span.jobTitle.hidden-phone a.jobTitle-link")
    job_title = job_title_element.text
    job_url = job_title_element.get_attribute('href')
    jobs.append({"Job-title": job_title, "URL": job_url})

print(json.dumps(jobs))

# Ensure the driver is quit after scraping
driver.quit()
