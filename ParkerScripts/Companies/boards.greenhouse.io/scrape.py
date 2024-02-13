from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
import sys
import json

# Retrieve target HTML file name from command line argument
target_html_file_name = sys.argv[1]

# Initialize WebDriver
driver = webdriver.Chrome()
driver.get(f"file:///{target_html_file_name}")

# Read the content of the file using BeautifulSoup
soup = BeautifulSoup(driver.page_source, 'html.parser')

# Find job opening blocks and job titles with URLs
job_opening_selectors = {
    "blocks": "div.opening",
    "title": "a[data-mapped='true']"
}

job_listings = []
for job_block in soup.select(job_opening_selectors["blocks"]):
    job_title_tag = job_block.select_one(job_opening_selectors["title"])
    if job_title_tag:
        job_title = job_title_tag.text.strip()
        job_url = job_title_tag['href'].strip()
        job_listings.append({"Job-title": job_title, "URL": job_url})

driver.quit()

# Print the result in JSON format
print(json.dumps(job_listings))