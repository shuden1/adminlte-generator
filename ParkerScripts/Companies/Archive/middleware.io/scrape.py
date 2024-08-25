from selenium import webdriver
import os
from dotenv import load_dotenv

load_dotenv()
from selenium.webdriver.common.by import By
import json
import sys

# STEP 1 results: Selectors for job openings
job_block_selector = 'ul.rec-job-info'
job_title_selector = 'li.rec-job-title a'
job_url_selector = 'li.rec-job-title a'

# STEP 2: Scraping script
def scrape_job_listings(html_file):
    # Setup Chrome options for Selenium
    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    options.add_argument('window-size=1200x600') # adjust as necessary

    # Initialize Chrome WebDriver
    driver = webdriver.Chrome(options=options)
    driver.get(f"file://{html_file}")

    # Find Job Opening elements
    job_elements = driver.find_elements(By.CSS_SELECTOR, job_block_selector)

    # Extract job titles and URLs
    job_listings = []
    for job_element in job_elements:
        title_element = job_element.find_element(By.CSS_SELECTOR, job_title_selector)
        url = title_element.get_attribute('href')
        title = title_element.text.strip()
        job_listings.append({"Job-title": title, "URL": url})

    # Quit the driver and return job listings as JSON
    driver.quit()

    return json.dumps(job_listings, indent=2)

# Expected input: python script.py /path/to/html/file.html
if __name__ == '__main__':
    html_file = sys.argv[1]
    print(scrape_job_listings(html_file))
