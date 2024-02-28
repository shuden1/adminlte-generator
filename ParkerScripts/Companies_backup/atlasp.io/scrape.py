from selenium import webdriver
from selenium.webdriver.common.by import By
import json
import sys

target_html_file = sys.argv[1]

driver = webdriver.Chrome()
driver.get(f"file://{target_html_file}")

job_blocks = driver.find_elements(By.CSS_SELECTOR, ".index-module--bottom--1y9gi h3.index-module--title--bDDbW")
jobs_data = []

for job_block in job_blocks:
    job_title = job_block.text.strip()
    # Assuming the job links are located at the same page, because no <a> tags found in provided snippets
    job_url = driver.current_url  # Placeholder URL since no actual URL was identified
    jobs_data.append({"Job-title": job_title, "URL": job_url})

driver.quit()

print(json.dumps(jobs_data))