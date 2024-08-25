from bs4 import BeautifulSoup
from selenium import webdriver
import os
from dotenv import load_dotenv

load_dotenv()
import sys
import json

# Step 1: Identify the EXACT HTML selectors including classes representing the blocks with Job Openings.
job_block_selectors = ".job-container"
job_title_selectors = ".job-content-header .job-title-and-category h2"
job_url_selectors = ".job-content-header .job-title-and-category a.mobile-apply-link"

# Step 2: Create a Python + Selenium script using the defined selectors.
def scrape_job_listings(html_file):
    # Initialize the Chrome webdriver
    driver = webdriver.Chrome()

    # Read the HTML content from file
    with open(html_file, 'r', encoding='utf-8') as file:
        html_content = file.read()

    # Use BeautifulSoup to parse the HTML content
    soup = BeautifulSoup(html_content, 'html.parser')

    # Find all job blocks
    job_blocks = soup.select(job_block_selectors)

    # Extracting job titles and their associated URLs
    jobs = []
    for job_block in job_blocks:
        title_element = job_block.select_one(job_title_selectors)
        url_element = job_block.select_one(job_url_selectors)
        if title_element and url_element:
            job_title = title_element.text.strip()
            job_url = url_element['href'].strip()
            jobs.append({"Job-title": job_title, "URL": job_url})

    # Close the driver
    driver.quit()

    # Output the results as JSON
    return json.dumps(jobs)

if __name__ == "__main__":
    html_file_name = sys.argv[1]  # The target HTML filename as an argument
    print(scrape_job_listings(html_file_name))
