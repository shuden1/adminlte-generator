from selenium import webdriver
import os
from dotenv import load_dotenv

load_dotenv()
from selenium.webdriver.common.by import By
import json
import sys

def scrape_job_listings(driver):
    job_listings_selector = '[data-qa="job-listing"]'
    job_title_selector = '[data-qa="job-title-link"]'

    job_elements = driver.find_elements(By.CSS_SELECTOR, job_listings_selector)
    job_listings = []
    for job_element in job_elements:
        title_element = job_element.find_element(By.CSS_SELECTOR, job_title_selector)
        title = title_element.text
        url = title_element.get_attribute('href')
        job_listings.append({"Job-title": title, "URL": url})

    return job_listings

if __name__ == '__main__':
    target_html_file = sys.argv[1]

    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    driver = webdriver.Chrome(options=options)

    driver.get(f"file:///{target_html_file}")

    jobs = scrape_job_listings(driver)
    print(json.dumps(jobs))

    driver.quit()
