from selenium import webdriver
import os
from dotenv import load_dotenv

load_dotenv()
from selenium.webdriver.common.by import By
import json
import sys

# Using arguments to get the target HTML file name
file_name = sys.argv[1]

# Initialize the Chrome WebDriver
driver = webdriver.Chrome()

# Open the local HTML file
driver.get(f"file://{file_name}")

# Define job title and URL selector (assuming they are contained within anchor tags inside a class that includes job listings)
job_title_url_selector = '.resumator-job-title-link'

# Initialize an empty list to store job listings
job_listings = []

# Find job listings within the HTML
job_elements = driver.find_elements(By.CSS_SELECTOR, job_title_url_selector)

# Extract the job titles and URLs
for job_element in job_elements:
    title = job_element.text
    url = job_element.get_attribute('href')
    job_listings.append({'Job-title': title, 'URL': url})

# Close the WebDriver
driver.quit()

# Output the job listings as JSON
print(json.dumps(job_listings))
