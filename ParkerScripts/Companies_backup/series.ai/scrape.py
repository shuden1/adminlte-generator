from selenium import webdriver
import sys
import json
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By

# The target HTML file name will be an argument sent from an external source through the console command
html_file_name = sys.argv[1]

# Start the Chrome session
driver = webdriver.Chrome()

# Open the local HTML file
driver.get(f"file://{html_file_name}")

# Read the HTML content using BeautifulSoup
soup = BeautifulSoup(driver.page_source, 'html.parser')

# Selectors identified from STEP 1
job_block_selector = 'div.sqs-block.html-block.sqs-block-html'
job_title_selector = 'h3 a'

# Find all blocks with job openings
job_blocks = soup.select(job_block_selector)

# Scrape job listings
job_listings = []
for block in job_blocks:
    job_title_elem = block.select_one(job_title_selector)
    if job_title_elem:
        job_title = job_title_elem.get_text(strip=True)
        job_url = job_title_elem['href']
        job_listings.append({"Job-title": job_title, "URL": job_url})

# Convert the list of job listings to JSON format
job_listings_json = json.dumps(job_listings)

# Close the driver
driver.quit()

# Return the JSON
print(job_listings_json)