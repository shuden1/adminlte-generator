from selenium import webdriver
import os
from dotenv import load_dotenv

load_dotenv()
import json
import sys

# Step 2: Creating the selenium script

# Extracting HTML file from console argument
file_name = sys.argv[1]

# Initiate selenium webdriver
driver = webdriver.Chrome()

# Open the local HTML file with the given file name
driver.get(f"file:///{file_name}")

# Scrape job listings using the selectors obtained in step 1
job_listings = driver.find_elements_by_class_name('job-listing')
jobs = []

for job_listing in job_listings:
    title_element = job_listing.find_element_by_tag_name('h3')
    url_element = title_element.find_element_by_tag_name('a')

    job = {
        "Job-title": title_element.text.strip(),
        "URL": url_element.get_attribute('href').strip()
    }

    jobs.append(job)

driver.quit()

# Output the result as JSON
print(json.dumps(jobs))
