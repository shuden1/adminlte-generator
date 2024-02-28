from selenium import webdriver
from selenium.webdriver.common.by import By
import json
import sys

# The target HTML file name is provided as an argument from an external source (command line argument)
html_file = sys.argv[1]

# Set up the Chrome WebDriver
driver = webdriver.Chrome()
driver.get(f'file://{html_file}')

# Using the defined selectors from Step 1 to identify blocks with Job Openings
job_listings = driver.find_elements(By.CSS_SELECTOR, "ul.divide-y")
jobs_data = []

# Loop through each listing to scrape job titles and URLs
for listing in job_listings:
    job_blocks = listing.find_elements(By.CSS_SELECTOR, "li")
    for job in job_blocks:
        job_title = job.find_element(By.CSS_SELECTOR, "h3.text-lg").text
        job_url = job.find_element(By.CSS_SELECTOR, "a").get_attribute('href')
        jobs_data.append({"Job-title": job_title, "URL": job_url})

# Close the WebDriver
driver.quit()

# Return scraped data as JSON
print(json.dumps(jobs_data))