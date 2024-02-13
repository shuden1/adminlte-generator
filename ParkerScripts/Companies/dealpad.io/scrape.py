from selenium import webdriver
from selenium.webdriver.common.by import By
import json
import sys

html_file_name = sys.argv[1]

driver = webdriver.Chrome()
driver.get(f"file:///{html_file_name}")

selectors = {
    "job_blocks": ".group.flex.cursor-pointer.flex-col.items-center.justify-start.rounded-2xl.border.border-transparent",
    "job_title": ".font-semibold",
    "job_url": ".text-sm.font-semibold.group-hover\\:text-dp-blue-400"
}

job_elements = driver.find_elements(By.CSS_SELECTOR, selectors['job_blocks'])

jobs = []

for job_element in job_elements:
    title_element = job_element.find_element(By.CSS_SELECTOR, selectors['job_title'])
    url_element = job_element.find_element(By.CSS_SELECTOR, selectors['job_url'])

    job = {
        "Job-title": title_element.text,
        "URL": url_element.get_attribute('href')
    }
    jobs.append(job)

driver.quit()

print(json.dumps(jobs))