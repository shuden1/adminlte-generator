from selenium import webdriver
import os
from dotenv import load_dotenv

load_dotenv()
from selenium.webdriver.common.by import By
import json
import sys

# STEP 1: Updated Selectors
job_block_selector = '.job-link-container .list-group li'
title_selector = 'li::text'
url_selector = 'a.btn'

# STEP 2: Selenium script
def scrape_job_listings(html_file):
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    driver = webdriver.Chrome(options=options)

    # Open the local HTML file
    driver.get(f"file:///{html_file}")

    # Find Job Opening blocks
    jobs = driver.find_elements(By.CSS_SELECTOR, job_block_selector)

    # Scrape job titles and URLs
    job_listings = []
    for job in jobs:
        title_element = job.find_element(By.CSS_SELECTOR, url_selector)
        job_title = job.text.replace(title_element.text, '').strip()
        job_url = title_element.get_attribute('href')
        job_listings.append({"Job-title": job_title, "URL": job_url})

    # Clean up and close the driver
    driver.quit()

    # Output the scraped job listings as JSON
    return json.dumps(job_listings)

if __name__ == "__main__":
    # Read target HTML filename from console argument
    target_html = sys.argv[1]

    # Scrape and print the job listings
    print(scrape_job_listings(target_html))
