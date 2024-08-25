from selenium import webdriver
import os
from dotenv import load_dotenv

load_dotenv()
import json
import sys

# Arguments
html_file = sys.argv[1]

# Webdriver
driver = webdriver.Chrome()

# Open HTML file
driver.get(f"file:///{html_file}")

# Selectors
job_list_selector = "ul.jobs-listing"
job_item_selector = "li.job-listing-item"
job_title_selector = "h3.job-title"
job_link_selector = "a"

# Fetch job listings
jobs = []
job_list = driver.find_element_by_css_selector(job_list_selector)
job_items = job_list.find_elements_by_css_selector(job_item_selector)
for job in job_items:
    title = job.find_element_by_css_selector(job_title_selector).text
    link = job.find_element_by_css_selector(job_link_selector).get_attribute('href')
    jobs.append({"Job-title": title, "URL": link})

# Close driver
driver.quit()

# Output
print(json.dumps(jobs))
