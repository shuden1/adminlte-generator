from selenium import webdriver
import os
from dotenv import load_dotenv

load_dotenv()
from selenium.webdriver.common.by import By
import json
import sys

def scrape_job_listings(html_file_name):
    # Initialize the Chrome WebDriver
    driver = webdriver.Chrome()

    # Open the local HTML file
    driver.get(f"file:///{html_file_name}")

    # Define the selectors for job blocks, job titles and URLs
    job_block_selector = '.et_pb_row'
    job_title_selector = '.et_pb_text h4'
    url_selector = '.et_pb_button_module_wrapper a'

    # Find all job listing blocks
    job_blocks = driver.find_elements(By.CSS_SELECTOR, job_block_selector)
    job_listings = []

    # Iterate through each block and extract job title and URL
    for job_block in job_blocks:
        try:
            job_title_element = job_block.find_element(By.CSS_SELECTOR, job_title_selector)
            job_title = job_title_element.text if job_title_element else None

            url_element = job_block.find_element(By.CSS_SELECTOR, url_selector)
            job_url = url_element.get_attribute('href') if url_element else None

            if job_title and job_url:
                job_listings.append({"Job-title": job_title, "URL": job_url})
        except Exception as e:
            continue

    # Clean up and close the browser
    driver.quit()

    # Return the job listings in JSON format
    return json.dumps(job_listings)

if __name__ == "__main__":
    html_file = sys.argv[1]
    print(scrape_job_listings(html_file))
