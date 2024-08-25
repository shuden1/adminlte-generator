from selenium import webdriver
import os
from dotenv import load_dotenv

load_dotenv()
from selenium.webdriver.common.by import By
import json
import sys

# Accept the target html file name through external arguments
target_html_file = sys.argv[1]

# Start a new instance of Chrome
with webdriver.Chrome() as driver:
    # Open the local HTML file in Chrome
    driver.get(f"file:///{target_html_file}")

    # Define the selectors based on the provided class attributes
    job_block_selector = 'wpex-post-cards-entry'
    job_title_selector = 'wpex-card-title'

    # Find all job opening blocks by the specified class name
    job_opening_blocks = driver.find_elements(By.CLASS_NAME, job_block_selector)

    # Prepare a list to hold job listing data
    job_listings = []

    # Iterate through the job opening blocks
    for job_block in job_opening_blocks:
        # Attempt to find the job title within the block
        job_titles = job_block.find_elements(By.CLASS_NAME, job_title_selector)

        for job_title in job_titles:
            # Attempt to find the <a> tag within the job title element
            a_tag = job_title.find_element(By.TAG_NAME, 'a')
            # Extract the text and URL from the <a> tag
            job_listings.append({
                "Job-title": a_tag.text,
                "URL": a_tag.get_attribute('href')
            })

    # Output the job listings as JSON
    print(json.dumps(job_listings))
