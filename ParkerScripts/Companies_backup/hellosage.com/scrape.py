from selenium import webdriver
import sys
import json

html_file = sys.argv[1]

# Using Selenium to scrape job listings
driver = webdriver.Chrome()
driver.get(f"file:///{html_file}")

# Selectors defined in Step 1
job_listing_selector = "div.job-item"
job_title_selector = "h2.job-title a"

# Find all job listings
job_listings = driver.find_elements_by_css_selector(job_listing_selector)
jobs_data = []

for job_listing in job_listings:
    job_title_element = job_listing.find_element_by_css_selector(job_title_selector)
    job_title = job_title_element.text
    job_url = job_title_element.get_attribute('href')

    jobs_data.append({
        "Job-title": job_title,
        "URL": job_url
    })

# Close the driver
driver.quit()

# Output data in JSON format
print(json.dumps(jobs_data))