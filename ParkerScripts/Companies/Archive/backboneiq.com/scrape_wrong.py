from selenium import webdriver
import os
from dotenv import load_dotenv

load_dotenv()
from selenium.webdriver.common.by import By
import json
import sys

def scrape_job_listings(html_file):
    # Initialize the WebDriver
    driver = webdriver.Chrome()
    driver.get(f"file:///{html_file}")

    # Define the selectors as per Step 1
    job_listing_selector = '.CareersGrid__JobBoard-sc-f66ztq-1 .job-listing'
    job_title_selector = 'h3.job-title'
    job_url_selector = 'a.job-url'

    job_listings = []

    # Find the job listings elements
    job_elements = driver.find_elements(By.CSS_SELECTOR, job_listing_selector)
    for job_element in job_elements:
        job_title_element = job_element.find_element(By.CSS_SELECTOR, job_title_selector)
        job_url_element = job_element.find_element(By.CSS_SELECTOR, job_url_selector)

        job_title = job_title_element.text.strip()
        job_url = job_url_element.get_attribute('href').strip()

        job_listings.append({"Job-title": job_title, "URL": job_url})

    driver.quit()

    return json.dumps(job_listings)

if __name__ == "__main__":
    html_filename = sys.argv[1]
    print(scrape_job_listings(html_filename))
