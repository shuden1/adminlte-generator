from selenium import webdriver
from selenium.webdriver.common.by import By
import json
import sys

# Define the exact selectors based on the HTML structure
job_block_selector = ".content-with-top-icon.title-with-link"
job_title_selector = "h4 a"

def extract_job_listings(driver):
    job_listings = []
    job_elements = driver.find_elements(By.CSS_SELECTOR, job_block_selector)
    for job_element in job_elements:
        job_title_element = job_element.find_element(By.CSS_SELECTOR, job_title_selector)
        title = job_title_element.text
        url = job_title_element.get_attribute('href')
        if url != "javascript:void(0)":  # Filter out invalid URLs
            job_listings.append({"Job-title": title, "URL": url})
    return job_listings

def main(html_file):
    # Initialize the Selenium Chrome driver
    driver = webdriver.Chrome()
    # Open the local HTML file
    driver.get(f"file:///{html_file}")

    # Extract job listings
    listings = extract_job_listings(driver)
    driver.quit()  # Close the browser

    # Output the results as JSON
    print(json.dumps(listings))

if __name__ == "__main__":
    # The path to the HTML file is provided as the first command-line argument
    html_file_path = sys.argv[1]
    main(html_file_path)