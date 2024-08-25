import sys
import json
from selenium import webdriver
import os
from dotenv import load_dotenv

load_dotenv()
from selenium.webdriver.common.by import By

# The target HTML file name is provided as a command-line argument
html_file_name = sys.argv[1]

# Set up the Selenium WebDriver for Chrome
driver = webdriver.Chrome()

# Open the local HTML file in the Chrome browser controlled by Selenium
driver.get(f"file:///{html_file_name}")

# Define the exact selectors for the job opening blocks, titles, and URLs
job_block_selector = 'section.content-editor'  # Placeholder selector
job_title_url_selector = 'section.content-editor a'  # Placeholder selector for titles and URLs together

# Initialize list to hold job listings
job_listings = []

# Locate job opening blocks
job_elements = driver.find_elements(By.CSS_SELECTOR, job_title_url_selector)

# Extract job titles and URLs
for job_element in job_elements:
    job_title = job_element.text
    job_url = job_element.get_attribute('href')
    job_listings.append({"Job-title": job_title, "URL": job_url})

# Close the browser
driver.quit()

# Output the job listings in the required JSON format
print(json.dumps(job_listings))
