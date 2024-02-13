from selenium import webdriver
from selenium.webdriver.common.by import By
import sys
import json

# The target HTML file name is received as an argument from an external source through the console command
target_html_file = sys.argv[1]

# Initialize the WebDriver for Chrome
driver = webdriver.Chrome()

try:
    # Open the HTML file
    driver.get(f"file://{target_html_file}")

    # Selectors for the blocks with job openings and for job titles & associated URLs as identified in step 1
    job_opening_blocks_selector = 'div.job-listing-collection-list'
    job_title_selector = 'h4.careers-list-heading'
    job_url_selector = 'a.link-lite-blue._16px._20p-top-padding.semi-bold-size'

    # Scraping all job listings
    job_listings = []
    job_blocks = driver.find_elements(By.CSS_SELECTOR, job_opening_blocks_selector)
    for job_block in job_blocks:
        titles = job_block.find_elements(By.CSS_SELECTOR, job_title_selector)
        urls = job_block.find_elements(By.CSS_SELECTOR, job_url_selector)
        for title, url in zip(titles, urls):
            job_listings.append({"Job-title": title.text, "URL": url.get_attribute('href')})

    # Convert to JSON and output
    print(json.dumps(job_listings))

finally:
    driver.quit()