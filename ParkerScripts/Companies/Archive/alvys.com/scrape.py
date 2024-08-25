from selenium import webdriver
import os
from dotenv import load_dotenv

load_dotenv()
from selenium.webdriver.common.by import By
import json
import sys

# Step 1 - Adjusted selectors after reviewing the HTML structure again
JOB_BLOCK_SELECTOR = '.elementor-section.elementor-inner-section.elementor-element.elementor-section-boxed.elementor-section-height-default.elementor-section-height-default'
JOB_TITLE_SELECTOR ='.elementor-col-50 h2.elementor-heading-title'
JOB_LINK_SELECTOR = '.elementor-col-50 a.elementor-button-link'

# Step 2 - Adjusted Selenium Script
def scrape_job_listings(html_file):
    # Setting up WebDriver
    driver = webdriver.Chrome()

    # Open the HTML file
    driver.get(f"file://{html_file}")

    # Scraping the job data
    job_listings = []

    job_blocks = driver.find_elements(By.CSS_SELECTOR, JOB_BLOCK_SELECTOR)
    for block in job_blocks:
        try:
            # Find the first h2 element for the job title within each job block
            title_elements = block.find_elements(By.CSS_SELECTOR, JOB_TITLE_SELECTOR)
            title_element = title_elements[0] if title_elements else None

            # Find the first link for the job within each job block
            link_elements = block.find_elements(By.CSS_SELECTOR, JOB_LINK_SELECTOR)
            link_element = link_elements[0] if link_elements else None

            if title_element and link_element:
                job_listings.append({"Job-title": driver.execute_script("return arguments[0].textContent;", title_element).strip(), "URL": link_element.get_attribute('href')})
            else:
                print("Missing title or link in this block, skipping.")
                continue
        except Exception as e:
            print(f"An error occurred: {e}")  # Print the exception for debugging
            continue

    # Closing the WebDriver
    driver.quit()

    # Output the result as JSON
    return json.dumps(job_listings)

if __name__ == "__main__":
    html_file = sys.argv[1]
    result = scrape_job_listings(html_file)
    print(result)
