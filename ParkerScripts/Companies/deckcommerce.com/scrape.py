from selenium import webdriver
from selenium.webdriver.common.by import By
import json
import sys

# Extract the target HTML file name from the command line argument
target_html_file = sys.argv[1]

# Initialize the Chrome WebDriver
driver = webdriver.Chrome()

# Open the target HTML file using the WebDriver
driver.get(f"file:///{target_html_file}")

# Set job opening block selector, job title and URL selector
job_opening_block_selector = '.hhs-list-con'
job_title_selector = '.hhs-list-con > div:nth-child(1) a div'
job_url_selector = '.hhs-list-con > div:nth-child(1) a'

# Find all job opening blocks
job_blocks = driver.find_elements(By.CSS_SELECTOR, job_opening_block_selector)
jobs_list = []

# Extract job titles and associated URLs from each job block
for job_block in job_blocks:
    title_element = job_block.find_element(By.CSS_SELECTOR, job_title_selector)
    url_element = job_block.find_element(By.CSS_SELECTOR, job_url_selector)
    job_title = title_element.get_attribute('innerText').strip()
    job_url = url_element.get_attribute('href').strip()
    jobs_list.append({"Job-title": job_title, "URL": job_url})

# Output the job listings in JSON format and close the driver
print(json.dumps(jobs_list))
driver.quit()