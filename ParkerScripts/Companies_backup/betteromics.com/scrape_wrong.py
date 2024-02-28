from selenium import webdriver
from selenium.webdriver.common.by import By
import json
import sys

# The CSS selector for the job listings container which is embedding another page
job_listing_selector = '.careers__StyledGreenhouseContainer-sc-1ni73e-0 iframe'

# Initialize Selenium WebDriver
driver = webdriver.Chrome()

# Prepare the script to accept the HTML file as an argument
target_html_file = sys.argv[1]
driver.get(f"file:///{target_html_file}")

# Wait for the iframe to load - Ideally, a proper wait condition should be applied
driver.implicitly_wait(10)

# Extract all job listing iframes using the determined selector
job_iframes = driver.find_elements(By.CSS_SELECTOR, job_listing_selector)
job_listings = []

for iframe in job_iframes:
    # Switch to the iframe context
    driver.switch_to.frame(iframe)
    
    # Inside the iframe, retrieve job titles and their respective URLs
    job_links = driver.find_elements(By.CSS_SELECTOR, 'a[data-qa="job-name"]')
    for link in job_links:
        job_title = link.text
        job_url = link.get_attribute('href')
        job_listings.append({
            "Job-title": job_title,
            "URL": job_url,
        })

    # Switch back to the main document before moving to the next iframe
    driver.switch_to.default_content()

driver.quit()

# Output job listings as JSON
jobs_json = json.dumps(job_listings)
print(jobs_json)