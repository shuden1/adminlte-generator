from selenium import webdriver
from selenium.webdriver.common.by import By
import json
import sys

# Get the HTML file name from the command line argument
html_file_name = sys.argv[1]

# Set up the Chrome webdriver
driver = webdriver.Chrome()

# Open the local HTML file
driver.get(f"file:///{html_file_name}")

# Scrape all job listings
job_elements = driver.find_elements(By.CSS_SELECTOR, ".eb-job-listings__listings .job-listing")
jobs_data = []

for job_element in job_elements:
    # Find the job title element within the job listing element
    job_title_element = job_element.find_element(By.CSS_SELECTOR, ".job-listing__title")
    # Extract the job title text
    job_title = job_title_element.text.strip()
    
    # Extract the job URL from the 'href' attribute of the anchor tag surrounding the job title
    job_url = job_element.get_attribute('href').strip()

    jobs_data.append({"Job-title": job_title, "URL": job_url})

driver.quit()

# Convert the list of dictionaries to JSON and print it
print(json.dumps(jobs_data))