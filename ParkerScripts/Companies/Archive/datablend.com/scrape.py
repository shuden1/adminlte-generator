from bs4 import BeautifulSoup
import sys
from selenium import webdriver
import os
from dotenv import load_dotenv

load_dotenv()
from selenium.webdriver.common.by import By
import json

# First we define the exact selectors
job_block_selector = '.row-fluid-wrapper.row-depth-1.row-number-3.dnd-row .hs_cos_wrapper_type_rich_text'
job_title_selector = 'a strong'
job_url_selector = 'a'

# Get the filename from the command line argument
html_filename = sys.argv[1]

# Step 2: Start the script
def main():
    # Setup Chrome WebDriver
    driver = webdriver.Chrome()

    # Open the local HTML file (ensure the environment is set to load local files)
    driver.get(f"file:///{html_filename}")

    # Find job listing elements based on the selectors
    job_elements = driver.find_elements(By.CSS_SELECTOR, job_block_selector)

    # Extract job titles and URLs
    jobs_data = []
    for job_element in job_elements:
        job_title_element = job_element.find_element(By.CSS_SELECTOR, job_title_selector)
        job_url_element = job_element.find_element(By.CSS_SELECTOR, job_url_selector)

        job_title = job_title_element.text if job_title_element else ''
        job_url = job_url_element.get_attribute('href') if job_url_element else ''

        jobs_data.append({"Job-title": job_title, "URL": job_url})

    # Close the browser
    driver.quit()

    # Output the JSON (use 'json.dumps()' for a string if needed)
    print(json.dumps(jobs_data))

# Run the script if this file is executed, not imported
if __name__ == "__main__":
    main()
