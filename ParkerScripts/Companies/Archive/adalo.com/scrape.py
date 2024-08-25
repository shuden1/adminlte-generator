from selenium import webdriver
import os
from dotenv import load_dotenv

load_dotenv()
from selenium.webdriver.common.by import By
import sys
import json

html_file = sys.argv[1]

options = webdriver.ChromeOptions()
options.add_argument(f"file://{html_file}")

driver = webdriver.Chrome(options=options)

job_openings_selector_class = "jobs_container"
job_title_and_url_selector = ".jobs_item.w-dyn-item .link-block-7"

driver.get(html_file)
job_listings = []

jobs = driver.find_elements(By.CSS_SELECTOR, job_title_and_url_selector)
for job in jobs:
    job_title = job.find_element(By.CSS_SELECTOR, ".jobs-title-text-block").text.strip()
    job_url = job.get_attribute('href').strip()
    job_listings.append({"Job-title": job_title, "URL": job_url})

driver.quit()

json_output = json.dumps(job_listings)
print(json_output)
