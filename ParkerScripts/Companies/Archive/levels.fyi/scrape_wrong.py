from selenium import webdriver
import os
from dotenv import load_dotenv

load_dotenv()
from selenium.webdriver.common.by import By
import json
import sys

# STEP 1: Obtain the correct selectors
job_opening_selector = 'li.company-sidebar_openRolesListItem__ydQ7P'
job_title_selector = 'a.MuiTypography-root.MuiTypography-body2.MuiLink-root.MuiLink-underlineHover'

# The selectors above are used in the following script for STEP 2.

# STEP 2: Script to scrape job listings using Selenium
def scrape_job_listings(html_file_path):
    # Initialize the Chrome WebDriver
    driver = webdriver.Chrome()

    # Open the local HTML file
    driver.get(f"file:///{html_file_path}")

    # Find all job opening elements using the defined selectors
    job_opening_elements = driver.find_elements(By.CSS_SELECTOR, job_opening_selector)

    # Initialize a list to hold job listings
    job_listings = []

    # Iterate over the job opening elements to extract job titles and URLs
    for job_element in job_opening_elements:
        title_element = job_element.find_element(By.CSS_SELECTOR, job_title_selector)
        title = title_element.text
        url = title_element.get_attribute('href')
        job_listings.append({"Job-title": title, "URL": url})

    # Close the WebDriver
    driver.quit()

    # Return the job listings as a JSON string
    return json.dumps(job_listings)


# The entry point for the script when it is executed
if __name__ == "__main__":
    # The HTML file path is taken from the command line argument
    html_file_path = sys.argv[1]

    # Scrape the job listings from the provided HTML file
    job_listings_json = scrape_job_listings(html_file_path)

    # Print out the job listings in JSON format
    print(job_listings_json)
