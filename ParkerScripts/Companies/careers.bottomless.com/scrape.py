from selenium import webdriver
from selenium.webdriver.common.by import By
import sys
import json

# STEP 1 output: The EXACT HTML CSS selectors
job_block_selector = '.notion-collection-list__item'
job_title_selector = '.notion-property__title'
job_url_selector = 'a.notion-link'

# Begin STEP 2
html_file = sys.argv[1]  # The HTML file is passed as the first argument from the external source

# setup the driver
driver = webdriver.Chrome()

# Proceed to scrape the data
driver.get(f'file:///{html_file}')
job_elements = driver.find_elements(By.CSS_SELECTOR, job_block_selector)
jobs_list = []

for job_element in job_elements:
    title_element = job_element.find_element(By.CSS_SELECTOR, job_title_selector)
    url_element = job_element.find_element(By.CSS_SELECTOR, job_url_selector)
    job_title = title_element.text.strip()
    job_url = url_element.get_attribute('href').strip()
    jobs_list.append({"Job-title": job_title, "URL": job_url})

# Printing the JSON data
print(json.dumps(jobs_list))

# Make sure to quit the driver
driver.quit()