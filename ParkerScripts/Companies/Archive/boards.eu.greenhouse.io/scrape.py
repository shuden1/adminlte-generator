from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
import json
import sys

# The target HTML file name is an argument sent from an external source
html_file_name = sys.argv[1]

# Start a new driver instance
service = Service()
driver = webdriver.Chrome(service=service)
driver.get(f"file:///{html_file_name}")

# Selectors defined in Step 1
job_openings_selector = ".opening"
job_title_selector = "a"
job_url_attribute = "href"

# Scrape all job listings
job_elements = driver.find_elements(By.CSS_SELECTOR, job_openings_selector)
jobs = [{"Job-title": job_element.find_element(By.CSS_SELECTOR, job_title_selector).text,
         "URL": job_element.find_element(By.CSS_SELECTOR, job_title_selector).get_attribute(job_url_attribute)}
        for job_element in job_elements]

# Return the scraped data as JSON
print(json.dumps(jobs))

# Clean up and close the driver
driver.quit()