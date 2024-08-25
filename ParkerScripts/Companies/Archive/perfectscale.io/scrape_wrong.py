from selenium import webdriver
import os
from dotenv import load_dotenv

load_dotenv()
from selenium.webdriver.common.by import By
import json
import sys

# Extract the file name from the command line argument
html_file_name = sys.argv[1]

# Set up the Chrome WebDriver
options = webdriver.ChromeOptions()
options.add_argument("--headless")
driver = webdriver.Chrome(options=options)

# Open the local HTML file
driver.get(f"file:///{html_file_name}")

# Selectors from the provided quote
job_block_selector = ".career-item.shadow-medium:not(.cc-hide)"
job_title_selector = ".career-title-heading .heading-style-h5"
job_url_selector = "a.button.is-secondary.is-small.w-button"

# Find Job opening blocks that are not hidden
job_blocks = driver.find_elements(By.CSS_SELECTOR, job_block_selector)

# Prepare the list to store job details
jobs_list = []

# Extract job titles and URLs from each job block
for job_block in job_blocks:
    # Find the title element, checking if it's not a placeholder 'Job Title'
    title_element = job_block.find_element(By.CSS_SELECTOR, job_title_selector)
    title = title_element.text
    if title != "Job Title":
        # Find the URL element only if the title is not a placeholder
        url_element = job_block.find_element(By.CSS_SELECTOR, job_url_selector)
        url = url_element.get_attribute('href')
        jobs_list.append({"Job-title": title, "URL": url})

driver.quit()

# Output the job details in JSON format
print(json.dumps(jobs_list))
