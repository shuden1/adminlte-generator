from selenium import webdriver
import os
from dotenv import load_dotenv

load_dotenv()
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
import threading
import sys
import json

# The target HTML file name comes from the external source as an argument
target_html_file = sys.argv[1]

# Initialising a headless webdriver
profile_folder_path = f"D:\\Mind\\CRA\\AI_Experiments\\Job_Crawlers\\Peter\\adminlte-generator\\chrome_profile\\{threading.get_ident()}"
service = ChromeService(executable_path=r""+os.getenv("CHROME_DRIVER_PATH")+"")
options = webdriver.ChromeOptions()
options.add_argument(f"user-data-dir={profile_folder_path}")
options.add_argument("--headless")
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")

driver = webdriver.Chrome(service=service, options=options)

# Going to the target HTML file
driver.get(f"file:///{target_html_file}")

# Using the previously identified selectors
job_elements = driver.find_elements(By.CSS_SELECTOR, ".menu li a[href*='/company/careers/']")

# Structure to store scraped data
jobs = []

for job_element in job_elements:
    job_title = job_element.text
    job_url = job_element.get_attribute("href")
    jobs.append({"Job-title": job_title, "URL": job_url})

# Ensuring the driver is quit after scraping
driver.quit()

# Output the jobs in JSON format
print(json.dumps(jobs))
