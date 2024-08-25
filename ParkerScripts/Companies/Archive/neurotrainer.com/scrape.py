from bs4 import BeautifulSoup
from selenium import webdriver
import os
from dotenv import load_dotenv

load_dotenv()
import json, sys

# Step 1: Identifying the selectors
# Job opening block selector
job_opening_block_selector = 'article.post'
# Job title and URL selector
job_title_selector = 'h2.entry-title a'

# Step 2: Python + Selenium script
def scrape_job_listings(html_file):
    # Initialize the WebDriver
    driver = webdriver.Chrome()

    # Load local HTML file
    driver.get(f'file:///{html_file}')

    # Use BeautifulSoup to parse the page
    soup = BeautifulSoup(driver.page_source, 'html.parser')

    # Find all job opening blocks
    job_opening_blocks = soup.select(job_opening_block_selector)

    # Scrape job titles and URLs
    job_listings = []
    for job_block in job_opening_blocks:
        job_title_tag = job_block.select_one(job_title_selector)
        if job_title_tag:
            job_title = job_title_tag.get_text(strip=True)
            job_url = job_title_tag['href']
            job_listings.append({"Job-title": job_title, "URL": job_url})

    # Close the WebDriver
    driver.quit()

    # Return the JSON result
    return json.dumps(job_listings)

if __name__ == '__main__':
    # The target HTML filename is the first argument from the console command
    html_filename = sys.argv[1]
    print(scrape_job_listings(html_filename))
