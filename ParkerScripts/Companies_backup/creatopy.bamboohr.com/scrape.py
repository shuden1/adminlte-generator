from bs4 import BeautifulSoup
from selenium import webdriver
import json
import sys

# The target HTML file name should be taken from the console command as the input parameter.
target_html_file = sys.argv[1]

# Step 1: Identifying the exact HTML selectors representing Job Openings blocks and associated URLs
# These selectors were identified by analyzing the provided HTML content:
job_openings_selector = 'div.jss-f8 main div.fab-CardContent ul li'
job_title_selector = 'a.jss-f65'
job_url_selector = 'a.jss-f65'

# Step 2: Selenium script to scrape all job listings using the selectors identified in Step 1
driver = webdriver.Chrome()
driver.get(f'file:///{target_html_file}')

soup = BeautifulSoup(driver.page_source, 'html.parser')
job_openings = soup.select(job_openings_selector)

jobs_list = []
for job in job_openings:
    title_element = job.select_one(job_title_selector)
    if title_element:
        job_title = title_element.text.strip()
        job_url = title_element['href']
        jobs_list.append({"Job-title": job_title, "URL": job_url})

driver.quit()

# Convert the list of jobs to JSON
jobs_json = json.dumps(jobs_list, ensure_ascii=False)
print(jobs_json)