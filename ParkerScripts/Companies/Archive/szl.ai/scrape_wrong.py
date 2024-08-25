import json
import sys
from selenium import webdriver
import os
from dotenv import load_dotenv

load_dotenv()
from selenium.webdriver.common.by import By

# WebDriver Selenium script to scrape job listings
def scrape_job_listings(file_name):
    driver = webdriver.Chrome()

    # Open the local HTML file
    driver.get(f"file:///{file_name}")

    # Selectors based on provided HTML structure
    job_blocks_selector = 'ul.accordion-items-container li.accordion-item'
    job_title_selector = 'span.accordion-item__title'
    job_url_selector = 'a'  # Assuming each job title is wrapped in an <a> tag

    # Find all job blocks
    job_blocks = driver.find_elements(By.CSS_SELECTOR, job_blocks_selector)
    jobs_data = []

    # Iterate over job blocks to extract job titles and URLs
    for job_block in job_blocks:
        # Extract the job title
        job_title_element = job_block.find_element(By.CSS_SELECTOR, job_title_selector)
        job_title = job_title_element.text.strip() if job_title_element else ""

        # Extract the job URL
        job_url_element = job_block.find_element(By.CSS_SELECTOR, job_url_selector)
        job_url = job_url_element.get_attribute('href').strip() if job_url_element else ""

        # Append job info to the list
        jobs_data.append({"Job-title": job_title, "URL": job_url})

    driver.quit()

    # Return the job data in JSON format
    return json.dumps(jobs_data)

if __name__ == "__main__":
    # The HTML file path is passed as a command-line argument
    html_file_path = sys.argv[1]
    job_listings_json = scrape_job_listings(html_file_path)
    print(job_listings_json)
