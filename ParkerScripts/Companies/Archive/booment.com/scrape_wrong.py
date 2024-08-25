import sys
from selenium import webdriver
import os
from dotenv import load_dotenv

load_dotenv()
from selenium.webdriver.common.by import By
import json

file_name = sys.argv[1]

driver = webdriver.Chrome()
driver.get(f"file:///{file_name}")

job_blocks = driver.find_elements(By.CSS_SELECTOR, "REPLACE_WITH_JOB_BLOCKS_SELECTOR")
jobs = []

for job_block in job_blocks:
    job_title_element = job_block.find_element(By.CSS_SELECTOR, "REPLACE_WITH_JOB_TITLE_SELECTOR")
    job_url_element = job_title_element.find_element(By.CSS_SELECTOR, "REPLACE_WITH_JOB_URL_SELECTOR")

    jobs.append({
        "Job-title": job_title_element.text,
        "URL": job_url_element.get_attribute('href')
    })

driver.quit()

print(json.dumps(jobs))
