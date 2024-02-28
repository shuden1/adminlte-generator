from selenium import webdriver
from selenium.webdriver.common.by import By
import json
import sys

# STEP 1: Selectors Identified
job_block_selector = ".job-listing-container .row .job-listing-job-item"
job_title_selector = ".job-title-column .job-item-title a"
job_url_selector = ".job-title-column .job-item-title a"

# STEP 2: Python + Selenium Script
def scrape_job_listings(html_file):
    # Set up Chrome WebDriver
    driver = webdriver.Chrome()
    driver.get(f"file://{html_file}")

    # Find all job listing elements
    job_elements = driver.find_elements(By.CSS_SELECTOR, job_block_selector)
    
    # Extract job titles and URLs
    job_listings = []
    for job_elem in job_elements:
        title_element = job_elem.find_element(By.CSS_SELECTOR, job_title_selector)
        job_title = title_element.text
        job_url = title_element.get_attribute("href")
        job_listings.append({"Job-title": job_title, "URL": job_url})
    
    driver.quit()
    
    # Return job listings in JSON format
    return json.dumps(job_listings)

if __name__ == "__main__":
    html_file_name = sys.argv[1]  # HTML file name is provided as an argument to the script
    print(scrape_job_listings(html_file_name))