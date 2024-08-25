from selenium import webdriver
import os
from dotenv import load_dotenv

load_dotenv()
from selenium.webdriver.common.by import By
import json
import sys

# Extract HTML file name from command line arguments
html_file_name = sys.argv[1]

def scrape_job_listings():
    # Initialize webdriver
    driver = webdriver.Chrome()

    # Open the local HTML file
    driver.get(f"file://{html_file_name}")

    # Define selectors from the analysis of the HTML file
    job_block_selector = "section.elementor-section" # Assuming the job listings are within <section> tags
    job_title_selector = "div.job-listing h3 a"     # Updated for job title within <h3> and <a> tags inside a div with a class .job-listing
    job_url_selector = "div.job-listing h3 a"       # Same as title selector, since the URL should be within the <a> tag's href attribute

    # Find job listing elements - assuming job listings are grouped in sections
    job_sections = driver.find_elements(By.CSS_SELECTOR, job_block_selector)

    # Initialize result list
    job_details = []

    for section in job_sections:
        # Filter out only sections that contain job listings
        job_listings = section.find_elements(By.CSS_SELECTOR, job_title_selector)
        if job_listings:
            # Extract job titles and URLs within the section
            for job in job_listings:
                job_details.append({
                    "Job-title": job.text.strip(),
                    "URL": job.get_attribute('href').strip()
                })

    # Close the browser
    driver.quit()

    # Return job details in JSON format
    return json.dumps(job_details, indent=2)

# Execute function and print results in the required format
print(scrape_job_listings())
