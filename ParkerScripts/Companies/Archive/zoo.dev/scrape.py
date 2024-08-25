from selenium import webdriver
import os
from dotenv import load_dotenv

load_dotenv()
from selenium.webdriver.common.by import By
import json
import sys

# STEP 1 results
job_listing_block_selector = "ul"
job_title_and_url_selector = "a.contents"

if len(sys.argv) != 2:
    print("The script requires exactly one argument for the HTML file name.")
    sys.exit(1)

# The name of the HTML file to scrape
html_file_name = sys.argv[1]

# STEP 2: Create the Selenium script
def scrape_job_listings(file_name):
    # Set up the Chrome WebDriver
    driver = webdriver.Chrome()

    # Load the local HTML file
    url = f'file:///{file_name}'
    driver.get(url)

    # Find all job listing blocks
    job_listing_blocks = driver.find_elements(By.CSS_SELECTOR, job_listing_block_selector)

    # Iterate through the blocks, and scrape the job titles and URLs
    job_listings = []
    for block in job_listing_blocks:
        job_titles_and_urls = block.find_elements(By.CSS_SELECTOR, job_title_and_url_selector)
        for job in job_titles_and_urls:
            title = job.text
            url = job.get_attribute('href')
            job_listings.append({"Job-title": title, "URL": url})

    # Close the WebDriver
    driver.quit()

    # Return the result as JSON
    return json.dumps(job_listings)

# Call the function and print out the results
print(scrape_job_listings(html_file_name))
