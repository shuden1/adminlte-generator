import json
import sys
from selenium import webdriver
import os
from dotenv import load_dotenv

load_dotenv()
from selenium.webdriver.common.by import By

def scrape_jobs(html_file):
    # Initialize the WebDriver
    driver = webdriver.Chrome()

    # Open the HTML file
    driver.get(f"file:///{html_file}")

    # Selectors from the BeautifulSoup analysis
    job_section_selector = ".wp-block-uagb-section"
    job_listing_selector = "h2 a"

    # Find all job sections
    job_sections = driver.find_elements(By.CSS_SELECTOR, job_section_selector)

    # Create a list to hold job title and URL pairs
    job_listings = []

    # Iterate over each job section to find job listings
    for section in job_sections:
        jobs = section.find_elements(By.CSS_SELECTOR, job_listing_selector)

        # Loop through each job to retrieve titles and URLs
        for job in jobs:
            title = job.text.strip()  # Get the job title text
            url = job.get_attribute('href')  # Get the job URL

            # Append job information if both title and URL exist
            if title and url:
                job_listings.append({
                    "Job-title": title,
                    "URL": url
                })

    # Close the WebDriver
    driver.quit()

    # Return the JSON-formatted job listings
    return json.dumps(job_listings)

if __name__ == "__main__":
    # Take the path to the HTML file as a command-line argument
    path_to_html = sys.argv[1]
    # Scrape jobs and print the results
    print(scrape_jobs(path_to_html))
