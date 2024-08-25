from selenium import webdriver
import os
from dotenv import load_dotenv

load_dotenv()
from selenium.webdriver.common.by import By
import json
import sys

# Step 2: Create a Python + Selenium script
def scrape_job_listings(html_file_path):
    # Start the Chrome WebDriver
    driver = webdriver.Chrome()
    try:
        # Open the HTML file in Chrome
        driver.get(f"file://{html_file_path}")

        # Use the selectors defined in Step 1 to find job listings
        job_listings = driver.find_elements(By.CSS_SELECTOR, "div.career__JobItemArea-qxr6gw-6 div.career__ToggleTitle-qxr6gw-0")
        job_titles_urls = []

        # Iterate over each job listing block and extract job title and URL
        for job in job_listings:
            job_title_element = job.find_element(By.CSS_SELECTOR, "h3.career__TitleText-qxr6gw-1")
            job_title = job_title_element.text
            # The structure does not contain URLs for individual job listings, so placeholder '#' is used
            job_url = '#'
            job_titles_urls.append({"Job-title": job_title, "URL": job_url})

        # Convert the job listings to JSON and print
        print(json.dumps(job_titles_urls))
    finally:
        # Close the WebDriver
        driver.quit()

# Get the target HTML file name as an argument from an external source
if len(sys.argv) != 2:
    print("Usage: script.py <path_to_html_file>")
else:
    html_file_path = sys.argv[1]
    scrape_job_listings(html_file_path)
