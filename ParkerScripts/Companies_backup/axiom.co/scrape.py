from selenium import webdriver
from selenium.webdriver.common.by import By
import sys
import json

def scrape_job_listings(html_file):
    # Open Chrome webdriver
    driver = webdriver.Chrome()
    driver.get(f"file:///{html_file}")

    # Selectors from Step 1 (updated to more generic)
    job_blocks_selector = "div.border-b.py-8"
    job_title_selector = "h3 span"
    job_url_selector = "a[href]"

    # Find all job blocks
    job_blocks = driver.find_elements(By.CSS_SELECTOR, job_blocks_selector)
    job_listings = []

    # Extract job title and URL from each job block
    for job_block in job_blocks:
        job_title_element = job_block.find_element(By.CSS_SELECTOR, job_title_selector)
        job_url_element = job_block.find_element(By.CSS_SELECTOR, job_url_selector)
        job_title = job_title_element.text
        job_url = job_url_element.get_attribute('href')
        job_listings.append({"Job-title": job_title, "URL": job_url})

    # Convert to JSON and print
    job_listings_json = json.dumps(job_listings)
    print(job_listings_json)

    # Close the webdriver
    driver.quit()

# Entry point
if __name__ == "__main__":
    html_file_path = sys.argv[1]
    scrape_job_listings(html_file_path)