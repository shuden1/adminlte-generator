from bs4 import BeautifulSoup
import json
import sys
from selenium import webdriver
from selenium.webdriver.common.by import By

# Retrieve the file name from the command line argument
file_name = sys.argv[1]

# STEP 1
# Process HTML with BeautifulSoup to identify the selectors
with open(file_name, 'r', encoding='utf-8') as file:
    soup = BeautifulSoup(file, 'html.parser')

    # Job listing block
    job_blocks_selector = 'div.flex.w-full.flex-row.justify-between.py-4'
    job_blocks = soup.select(job_blocks_selector)
    
    # Job title and URL
    job_title_selector = 'div.ycdc-with-link-color.pr-4.text-lg.font-bold > a'
    
    # Proceed only if job titles and URLs are found
    job_titles_urls = []
    for job_block in job_blocks:
        job_anchor = job_block.select_one(job_title_selector)
        if job_anchor:
            job_titles_urls.append({
                'Job-title': job_anchor.get_text(strip=True),
                'URL': job_anchor['href']
            })

# STEP 2
# Implement the Selenium script
driver = webdriver.Chrome()

# Open the HTML file with the driver
driver.get("file://" + file_name)

# Scrape the job listings
job_listings = []
job_blocks_elements = driver.find_elements(By.CSS_SELECTOR, job_blocks_selector)
for job_block_element in job_blocks_elements:
    job_anchor_element = job_block_element.find_element(By.CSS_SELECTOR, job_title_selector)
    job_listings.append({
        "Job-title": job_anchor_element.text,
        "URL": job_anchor_element.get_attribute('href')
    })

driver.close()

# Return the JSON result
print(json.dumps(job_listings))