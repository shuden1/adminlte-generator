import json
import sys
from selenium import webdriver
import os
from dotenv import load_dotenv

load_dotenv()
from selenium.webdriver.common.by import By

# Use the selectors identified from the BeautifulSoup analysis
# Replace '.job-listing-class' and '.job-title-class' with the actual classes
job_listing_selector = '.job-listing-class'
job_title_selector = '.job-title-class a'

def extract_job_listings(driver, html_file_path):
    driver.get(f"file:///{html_file_path}")
    job_elements = driver.find_elements(By.CSS_SELECTOR, job_listing_selector)
    job_listings = []

    for job_elem in job_elements:
        title_element = job_elem.find_element(By.CSS_SELECTOR, job_title_selector)
        job_title = title_element.text.strip()
        job_url = title_element.get_attribute('href').strip()
        job_listings.append({'Job-title': job_title, 'URL': job_url})

    return job_listings

def main(html_file_path):
    options = webdriver.ChromeOptions()
    options.headless = True
    driver = webdriver.Chrome(options=options)
    try:
        job_listings = extract_job_listings(driver, html_file_path)
        print(json.dumps(job_listings))
    finally:
        driver.quit()

if __name__ == '__main__':
    html_file_path = sys.argv[1]
    main(html_file_path)
