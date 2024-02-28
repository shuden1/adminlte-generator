from selenium import webdriver
from selenium.webdriver.common.by import By
import json
import sys

# Argument given from an external source
html_file = sys.argv[1]

# Options for ChromeDriver
options = webdriver.ChromeOptions()
options.add_argument("--start-maximized")

# WebDriver
driver = webdriver.Chrome(options=options)

# Open the HTML file
driver.get(f"file://{html_file}")

# Selectors from Step 1
job_blocks_selector = '.job'
job_title_selector = '.job-wrap h2'
job_url_selector = '.job-wrap'

# Scrape the job listings
job_listings = []
job_blocks = driver.find_elements(By.CSS_SELECTOR, job_blocks_selector)
for job_block in job_blocks:
    # Extract job title and URL
    title_element = job_block.find_element(By.CSS_SELECTOR, job_title_selector)
    link_element = job_block.find_element(By.CSS_SELECTOR, job_url_selector)
    job_title = title_element.get_attribute('innerText').strip()
    job_url = link_element.get_attribute('href').strip()
    
    # Add job to the list
    job_listings.append({"Job-title": job_title, "URL": job_url})

# Close driver
driver.quit()

# Return JSON output
print(json.dumps(job_listings))