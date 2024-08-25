from selenium import webdriver
import os
from dotenv import load_dotenv

load_dotenv()
from selenium.webdriver.common.by import By
import json
import sys

# The target HTML file name comes from the first argument of the command line
html_file_name = sys.argv[1]

driver = webdriver.Chrome()
driver.get(f"file:///{html_file_name}")

job_blocks_selector = ".jobs_item.w-dyn-item"
job_title_selector = ".position-name div"
job_url_selector = ".jobs_link"

jobs = []

# Find all job opening blocks
job_blocks = driver.find_elements(By.CSS_SELECTOR, job_blocks_selector)
for job_block in job_blocks:
    # Find the job title and URL within each job opening block
    job_title = job_block.find_element(By.CSS_SELECTOR, job_title_selector).text
    job_url = job_block.find_element(By.CSS_SELECTOR, job_url_selector).get_attribute("href")

    # Append job details to the jobs list
    jobs.append({"Job-title": job_title, "URL": job_url})

driver.quit()

# Return jobs details in JSON format
print(json.dumps(jobs))
