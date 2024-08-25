from selenium import webdriver
import os
from dotenv import load_dotenv

load_dotenv()
from selenium.webdriver.common.by import By
import json
import sys

# Selector for job opening blocks
job_block_selector = ".awsm-job-listing-item"
# Selectors for job titles and URLs within job opening blocks
job_title_selector = "h2.awsm-job-post-title"
job_url_selector = "a.awsm-job-item"

# STEP 2: Selenium script
def scrape_job_listings(html_file):
    # Set up the Selenium driver
    driver = webdriver.Chrome()
    # Open the local HTML file
    driver.get(f"file://{html_file}")

    # Find all job opening blocks
    job_blocks = driver.find_elements(By.CSS_SELECTOR, job_block_selector)

    # Initialize a list to store job information
    job_listings = []

    for job in job_blocks:
        # Extract job title and job URL
        title = job.find_element(By.CSS_SELECTOR, job_title_selector).text
        url = job.find_element(By.CSS_SELECTOR, job_url_selector).get_attribute('href')
        # Append a dictionary with the job details to the list
        job_listings.append({"Job-title": title, "URL": url})

    # Convert the list of jobs to JSON
    json_result = json.dumps(job_listings)

    # Quit the Selenium driver
    driver.quit()

    # Return the JSON result
    return json_result

if __name__ == "__main__":
    # The target HTML file name is an argument sent from the console
    target_html = sys.argv[1]
    # Scrape and print the job listings
    print(scrape_job_listings(target_html))
