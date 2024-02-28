from selenium import webdriver
from selenium.webdriver.common.by import By
import json
import sys

# Retrieve the target HTML file name from the command line argument
target_html_file = sys.argv[1]

# Step 1: Define the selectors (Example selectors as per instruction)
job_block_selector = ".jobs-list .job"
job_title_selector = ".job-title"
job_url_data_attribute = "data-link"

# Step 2: Create a Selenium script to scrape job listings
def scrape_job_listings(html_file):
    driver = webdriver.Chrome()
    driver.get(f"file://{html_file}")
    
    job_elements = driver.find_elements(By.CSS_SELECTOR, job_block_selector)
    job_listings = []
    
    for job_el in job_elements:
        job_title = job_el.find_element(By.CSS_SELECTOR, job_title_selector).text
        job_url = job_el.get_attribute(job_url_data_attribute)
        
        job_listings.append({"Job-title": job_title, "URL": job_url})
    
    driver.quit()
    return json.dumps(job_listings)

# Execute scraping function with given HTML file
scraped_data = scrape_job_listings(target_html_file)
print(scraped_data)