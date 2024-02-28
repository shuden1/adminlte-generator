from selenium import webdriver
from selenium.webdriver.common.by import By
import json
import sys

# Grab the HTML file name from the arguments
html_file = sys.argv[1]

# Set up the Chrome WebDriver
driver = webdriver.Chrome()

# Open the target HTML file
driver.get(f"file://{html_file}")

# Define the selector for the job openings block
job_openings_selector = ".jobs-collection_item"
# Define the selectors for job titles and their associated URLs
job_title_selector = ".display-text-size-small"
job_url_selector = ".btn.primary.w-button"

# Find all job openings blocks
job_openings_blocks = driver.find_elements(By.CSS_SELECTOR, job_openings_selector)
jobs_list = []

# Iterate over each job opening block to extract the job titles and URLs
for job_block in job_openings_blocks:
    job_title_element = job_block.find_element(By.CSS_SELECTOR, job_title_selector)
    job_title = job_title_element.text.strip()

    job_url_element = job_block.find_element(By.CSS_SELECTOR, job_url_selector)
    job_url = job_url_element.get_attribute('href').strip()

    jobs_list.append({"Job-title": job_title, "URL": job_url})

# Output the jobs in JSON format
print(json.dumps(jobs_list))

# Close the WebDriver
driver.quit()