from selenium import webdriver
from selenium.webdriver.common.by import By
import json
import sys

# The target HTML file name is an argument sent from an external source through the console command as the single input parameter.
html_file_name = sys.argv[1]

# Set up the Chrome WebDriver
driver = webdriver.Chrome()

# Open the target HTML file
driver.get(f"file:///{html_file_name}")

# Identifying the exact HTML selectors representing the blocks with Job Openings and the exact selectors for job titles and their associated URLs
job_blocks_selector = '.gb-inside-container ul li'
job_title_selector = 'a'
job_url_attribute = 'href'

# Initialize a list to hold all job listings
jobs_list = []

# Find all job opening blocks
job_openings = driver.find_elements(By.CSS_SELECTOR, job_blocks_selector)
for job in job_openings:
    # Extract the job title and URL
    title = job.find_element(By.CSS_SELECTOR, job_title_selector).text.strip()
    url = job.find_element(By.CSS_SELECTOR, job_title_selector).get_attribute(job_url_attribute).strip()

    # Append a dictionary with the job title and URL to the list
    jobs_list.append({'Job-title': title, 'URL': url})

# Close the browser
driver.quit()

# Output the jobs list in JSON format
print(json.dumps(jobs_list))
