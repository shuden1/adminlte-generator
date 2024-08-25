from selenium import webdriver
import os
from dotenv import load_dotenv

load_dotenv()
import json
import sys

# Step 1 Extract Selectors
job_block_selector = '.sqs-block-content .sqs-html-content'
job_title_selector = 'h3 span'
job_url_selector = 'a'

# Step 2 Selenium script
def scrape_job_listings(html_file_path):
    # Setup Selenium WebDriver
    driver = webdriver.Chrome()
    driver.get(f"file:///{html_file_path}")

    # Find job listing elements
    job_blocks = driver.find_elements_by_css_selector(job_block_selector)
    job_listings = []

    for block in job_blocks:
        titles = block.find_elements_by_css_selector(job_title_selector)
        urls = block.find_elements_by_css_selector(job_url_selector)

        for title, link in zip(titles, urls):
            job_listings.append({"Job-title": title.text, "URL": link.get_attribute('href')})

    driver.quit()

    # Output as JSON
    print(json.dumps(job_listings))

if __name__ == "__main__":
    target_html_file = sys.argv[1]
    scrape_job_listings(target_html_file)
