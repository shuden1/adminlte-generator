from selenium import webdriver
from selenium.webdriver.common.by import By
import json
import sys

html_file = sys.argv[1]

driver = webdriver.Chrome()
driver.get(f"file:///{html_file}")

job_data = []
jobs = driver.find_elements(By.CSS_SELECTOR, 'a._container_j2da7_1')

for job in jobs:
    title_element = job.find_element(By.CSS_SELECTOR, 'h3._title_1qwfy_383')
    title = title_element.text
    url = job.get_attribute('href')
    job_data.append({"Job-title": title, "URL": url})

driver.quit()

print(json.dumps(job_data))