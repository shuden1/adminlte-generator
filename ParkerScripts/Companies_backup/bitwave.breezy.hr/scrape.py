from selenium import webdriver
from selenium.webdriver.common.by import By
import json
import sys

# Step 1: Identifying the job opening blocks and exact selectors
job_block_selector = '.positions-container ul.positions > li.position'
job_title_selector = 'h2'
job_url_selector = 'a'

# Step 2: Create a Python + Selenium script
filename = sys.argv[1]

driver = webdriver.Chrome()

try:
    # Open the HTML file
    driver.get(f'file:///{filename}')
    
    # Find all job elements
    job_elements = driver.find_elements(By.CSS_SELECTOR, job_block_selector)
    
    # Extract job titles and their associated URLs
    job_listings = []
    for job_element in job_elements:
        title_element = job_element.find_element(By.CSS_SELECTOR, job_title_selector)
        url_element = job_element.find_element(By.CSS_SELECTOR, job_url_selector)
        
        job_listings.append({
            "Job-title": title_element.text,
            "URL": url_element.get_attribute('href')
        })
    
    # Close the browser
    driver.quit()
    
    # Convert job listings to JSON format and print
    print(json.dumps(job_listings))
except Exception as e:
    driver.quit()
    raise e