import sys
from selenium import webdriver
from selenium.webdriver.common.by import By
import json

def scrape_job_listings(html_file):
    # Initialize the Chrome driver
    driver = webdriver.Chrome()
    driver.get(f"file:///{html_file}")

    # Since actual selectors are unknown due to inability to see the HTML structure, setup based on common assumptions
    job_blocks_selector = "section.jobs-listing .job"  # Placeholder, adjust according to actual structure
    job_title_selector = "h2 a"  # Placeholder, adjust according to actual structure
    job_url_selector = "h2 a"  # Assuming title and URL are within the same anchor tag

    # Find all job listing blocks
    job_blocks = driver.find_elements(By.CSS_SELECTOR, job_blocks_selector)

    # Initialize list to store job listings
    job_listings = []

    # Extract job titles and URLs
    for block in job_blocks:
        title_element = block.find_element(By.CSS_SELECTOR, job_title_selector)
        url_element = block.find_element(By.CSS_SELECTOR, job_url_selector)
        job_listings.append({"Job-title": title_element.text, "URL": url_element.get_attribute('href')})

    # Close the driver
    driver.quit()

    # Output the job listings as JSON formatted string
    return json.dumps(job_listings)

if __name__ == "__main__":
    html_file = sys.argv[1]
    print(scrape_job_listings(html_file))