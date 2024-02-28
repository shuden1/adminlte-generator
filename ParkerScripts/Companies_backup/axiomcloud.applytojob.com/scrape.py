from selenium import webdriver
from selenium.webdriver.common.by import By
import json
import sys

# The target HTML file name comes from the command line argument
target_html_file = sys.argv[1]

# Setup Chrome webdriver
driver = webdriver.Chrome()

# Open the target HTML file
driver.get(f"file:///{target_html_file}")

# Using the selectors identified in step 1 to find job listings
job_blocks_selector = ".jobs-list .list-group-item"
job_titles_selector = "h4 > a"

# Find all job listings using the defined selectors
job_listings = driver.find_elements(By.CSS_SELECTOR, job_blocks_selector)

# Process and gather job titles and urls into a list
jobs = []
for job in job_listings:
    title_element = job.find_element(By.CSS_SELECTOR, job_titles_selector)
    jobs.append({"Job-title": title_element.text, "URL": title_element.get_attribute("href")})

# Close the driver
driver.quit()

# Return the JSON result
print(json.dumps(jobs))