from bs4 import BeautifulSoup
import json
import sys
from selenium import webdriver
import os
from dotenv import load_dotenv

load_dotenv()
from selenium.webdriver.common.by import By

# Step 1: Identifying the EXACT HTML selectors
job_block_selector = ".list-group-item"
job_title_selector = "h4 > a"
job_url_selector = "h4 > a"


# Step 2: Python + Selenium script
def scrape_job_listings(html_file):
    # Step 2.2: Initialize the WebDriver
    driver = webdriver.Chrome()

    # Step 2.3: Load the HTML file
    driver.get(f"file://{html_file}")

    # Step 2.3: Scrape the job listings
    job_blocks = driver.find_elements(By.CSS_SELECTOR, job_block_selector)
    job_listings = []

    for job_block in job_blocks:
        title_element = job_block.find_element(By.CSS_SELECTOR, job_title_selector)
        job_title = title_element.text
        job_url = title_element.get_attribute('href')
        job_listings.append({"Job-title": job_title, "URL": job_url})

    # Step 2.4: Close the WebDriver
    driver.quit()

    # Step 2.5: Return the JSON format
    return json.dumps(job_listings)


if __name__ == "__main__":
    # Step 2.1: The target HTML file is an argument from the console
    html_filename = sys.argv[1]
    print(scrape_job_listings(html_filename))
