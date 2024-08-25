from selenium import webdriver
import os
from dotenv import load_dotenv

load_dotenv()
from selenium.webdriver.common.by import By
import json
import sys

html_file = sys.argv[1]

driver = webdriver.Chrome()
driver.get(f"file:///{html_file}")

jobs = []

# Using JavaScript to access Greenhouse iframe content
driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
iframe = driver.wait.until(lambda d: d.find_element(By.ID, 'grnhse_iframe'))
driver.switch_to.frame(iframe)
job_elements = driver.find_elements(By.CSS_SELECTOR, 'div.opening a')

for job_element in job_elements:
    title = job_element.text
    url = job_element.get_attribute('href')
    jobs.append({"Job-title": title, "URL": url})

driver.quit()

print(json.dumps(jobs))
