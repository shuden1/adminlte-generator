from selenium import webdriver
import os
from dotenv import load_dotenv

load_dotenv()
from selenium.webdriver.common.by import By
import json
import sys

# STEP 1: Define the EXACT HTML selectors
job_block_selector = '.notion-table-view-cell'
job_title_selector = '[data-block-id] div div a:not([class])'
job_url_selector = '[data-block-id] div div a:not([class])'

# STEP 2: Create a Python + Selenium script
def extract_job_listings(html_file):
    # STEP 2.1: Initialize the Chrome driver
    driver = webdriver.Chrome()

    results = []

    try:
        # STEP 2.2: Load the HTML file
        driver.get(f"file://{html_file}")

        # STEP 2.3: Find job blocks and extract titles and URLs
        job_blocks = driver.find_elements(By.CSS_SELECTOR, job_block_selector)
        for job_block in job_blocks:
            job_title_elements = job_block.find_elements(By.CSS_SELECTOR, job_title_selector)
            job_url_elements = job_block.find_elements(By.CSS_SELECTOR, job_url_selector)

            for job_title_element, job_url_element in zip(job_title_elements, job_url_elements):
                job_title = job_title_element.text.strip()
                job_url = job_url_element.get_attribute('href')
                if job_title and job_url.startswith('http'):
                    results.append({"Job-title": job_title, "URL": job_url})
    finally:
        # STEP 2.4: Close the driver
        driver.quit()

    # STEP 2.5: Print out the results in JSON format
    print(json.dumps(results))

if __name__ == "__main__":
    html_file_name = sys.argv[1]
    extract_job_listings(html_file_name)
