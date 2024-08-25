from selenium import webdriver
import os
from dotenv import load_dotenv

load_dotenv()
from selenium.webdriver.common.by import By
import sys
import json

# Start the Chrome WebDriver
driver = webdriver.Chrome()

# Define the selectors for the job blocks and job titles/URLs
job_listing_selector = ".flex-row.items-start.p-4.space-x-2.group"
job_title_url_selector = "a.font-semibold.truncate"

def extract_job_listings(driver, job_listing_selector, job_title_url_selector):
    # Find all job listing blocks
    job_listings = driver.find_elements(By.CSS_SELECTOR, job_listing_selector)
    jobs_output = []

    # Extract job titles and URLs
    for job_listing in job_listings:
        job_title_elements = job_listing.find_elements(By.CSS_SELECTOR, job_title_url_selector)
        for job_title_element in job_title_elements:
            job_title = job_title_element.text
            job_url = job_title_element.get_attribute('href')
            if job_title and job_url:
                jobs_output.append({"Job-title": job_title, "URL": job_url})

    return jobs_output

def main():
    # Get the filename from the command line argument
    html_file_path = sys.argv[1]

    # Open the local HTML file
    driver.get(f"file:///{html_file_path}")

    # Extract information and print in JSON format
    jobs = extract_job_listings(driver, job_listing_selector, job_title_url_selector)
    print(json.dumps(jobs))

    # Quit the driver
    driver.quit()

if __name__ == "__main__":
    main()
