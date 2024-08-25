from selenium import webdriver
import os
from dotenv import load_dotenv

load_dotenv()
from selenium.webdriver.common.by import By
import sys
import json

# Step 1 selectors
job_listings_selector = '.et_pb_section_5 .et_pb_row_10'
job_title_selector = 'a'

# Step 2 code
def scrape_job_listings(file_path):
    # Starting the Chrome WebDriver
    options = webdriver.ChromeOptions()
    options.add_argument('--disable-gpu')
    options.add_argument('--headless')
    driver = webdriver.Chrome(options=options)

    # Prepare URL from file path
    url = f"file:///{file_path}"

    # Open the file via the driver
    driver.get(url)

    # Locate the job listings block and job titles
    job_listings = []
    job_blocks = driver.find_elements(By.CSS_SELECTOR, job_listings_selector)
    for block in job_blocks:
        job_links = block.find_elements(By.CSS_SELECTOR, job_title_selector)
        for job_link in job_links:
            job_title = job_link.text.strip()
            job_url = job_link.get_attribute('href')
            job_listings.append({'Job-title': job_title, 'URL': job_url})

    driver.quit()
    return json.dumps(job_listings)

# Execution
if __name__ == '__main__':
    html_file_name = sys.argv[1]
    results = scrape_job_listings(html_file_name)
    print(results)
