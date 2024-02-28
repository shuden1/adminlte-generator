from selenium import webdriver
from selenium.webdriver.common.by import By
import json
import sys

html_file_name = sys.argv[1]

driver = webdriver.Chrome()
driver.get(f"file:///{html_file_name}")

job_blocks_selector = ".greenhouse-jobs-item"
job_title_selector = ".greenhouse-jobs-item--title"
job_link_selector = ".avia-button"

job_elements = driver.find_elements(By.CSS_SELECTOR, job_blocks_selector)

job_listings = []

for job_element in job_elements:
    title_element = job_element.find_element(By.CSS_SELECTOR, job_title_selector)
    link_element = job_element.find_element(By.CSS_SELECTOR, job_link_selector)
    job_title = title_element.text.strip()
    job_url = link_element.get_attribute('href').strip()
    job_listings.append({"Job-title": job_title, "URL": job_url})

driver.quit()

print(json.dumps(job_listings))