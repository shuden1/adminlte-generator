import sys
from selenium import webdriver
import os
from dotenv import load_dotenv

load_dotenv()
from selenium.webdriver.common.by import By
import json

def scrape_job_listings(filename):
    # Setup the Chrome WebDriver
    driver = webdriver.Chrome()

    try:
        # Open the HTML file with the provided filename
        driver.get(f"file:///{filename}")

        # Job Selectors (as identified in Step 1)
        job_block_selector = "ul.orange-bullets"
        job_title_selector = "li a.blue"

        # Scrape the job listings
        job_blocks = driver.find_elements(By.CSS_SELECTOR, job_block_selector)
        job_listings = []

        for block in job_blocks:
            jobs = block.find_elements(By.CSS_SELECTOR, job_title_selector)
            for job in jobs:
                job_title = job.text
                job_url = job.get_attribute("href")
                job_listings.append({"Job-title": job_title, "URL": job_url})

        # Output the job listings in JSON format
        return json.dumps(job_listings)

    finally:
        # Close the WebDriver
        driver.quit()

# Assuming the filename argument is being passed through the console command (sys.argv[1])
if __name__ == '__main__':
    target_file = sys.argv[1]
    print(scrape_job_listings(target_file))
