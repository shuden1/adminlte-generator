from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
import json
import sys

# STEP 1: BeautifulSoup usage to define the selectors - not executable in this environment, it's just a clarification.
# This code is only to illustrate the process, it is not meant to be run.

'''
html_content = open('your_html_file.html', 'r').read()  # Hypothetical reading of the HTML file content.
soup = BeautifulSoup(html_content, 'html.parser')

# Identify the blocks with Job Openings
blocks = soup.select('.jobs_VG2e > a.job_M3eU')

# Identifying job title and associated URL selectors
for block in blocks:
    title_selector = '.jobName_IiL5'
    title = block.select_one(title_selector).text
    url = block['href']
'''

# STEP 2: Python + Selenium script
if len(sys.argv) != 2:
    sys.exit("Usage: script.py <HTML_FILE_NAME>")

html_file_name = sys.argv[1]

driver = webdriver.Chrome()
driver.get(f"file://{html_file_name}")

# Using the EXACT HTML selectors identified in Step 1
jobs = driver.find_elements(By.CSS_SELECTOR, '.jobs_VG2e > a.job_M3eU')

job_listings = []
for job in jobs:
    title = job.find_element(By.CSS_SELECTOR, '.jobName_IiL5').text
    url = job.get_attribute('href')
    job_listings.append({"Job-title": title, "URL": url})

driver.quit()

# Output the job listings as JSON
print(json.dumps(job_listings))