from selenium import webdriver
import os
from dotenv import load_dotenv

load_dotenv()
from selenium.webdriver.common.by import By
import json
import sys

# Receive the HTML file name as a command line argument
html_file = sys.argv[1]

# Initialize the Chrome WebDriver
driver = webdriver.Chrome()

# Load the HTML file
driver.get(f"file:///{html_file}")

# Define the selectors for the job opening blocks, job titles, and URLs
job_block_selector = '.careers_open_position_section'
job_title_selector = 'h3'
job_link_selector = 'a'

# Find job listing elements
job_blocks = driver.find_elements(By.CSS_SELECTOR, job_block_selector)

# List to hold job titles and URLs
jobs = []

# Extract job titles and URLs from each job block
for block in job_blocks:
    job_titles = block.find_elements(By.CSS_SELECTOR, job_title_selector)
    job_links = block.find_elements(By.CSS_SELECTOR, job_link_selector)
    for title, link in zip(job_titles, job_links):
        # Ensure the job title and URL are not empty and add them to the jobs list
        if title.text and link.get_attribute('href'):
            jobs.append({
                "Job-title": title.text,
                "URL": link.get_attribute('href')
            })

# Return the JSON representation of job titles and URLs
print(json.dumps(jobs))

# Close the WebDriver
driver.quit()
