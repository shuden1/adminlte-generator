from selenium import webdriver
from selenium.webdriver.common.by import By
import json
import sys

# Constants based on STEP 1 findings
JOB_LISTING_BLOCK_SELECTOR = ".zn_textbox.left.eluidbfa40e87 .zn_description"
JOB_TITLE_SELECTOR = "h1 span"
JOB_URL_SELECTOR = "a"

def scrape_job_listings(html_file):
    # Initialize the driver
    driver = webdriver.Chrome()
    
    # Open the local HTML file
    driver.get(f"file:///{html_file}")
    
    # Find the job listings block
    job_listing_block = driver.find_element(By.CSS_SELECTOR, JOB_LISTING_BLOCK_SELECTOR)
    
    # Extract job titles and URLs
    job_titles = job_listing_block.find_elements(By.CSS_SELECTOR, JOB_TITLE_SELECTOR)
    job_urls = job_listing_block.find_elements(By.CSS_SELECTOR, JOB_URL_SELECTOR)
    
    job_listings = []
    
    # Combine titles and URLs into job listings
    for title_element, url_element in zip(job_titles, job_urls):
        job_title = title_element.text.strip() if title_element.text else "No title found"
        job_url = url_element.get_attribute('href') if url_element.get_attribute('href') else "No URL found"
        job_listings.append({"Job-title": job_title, "URL": job_url})
    
    # Convert the job listings to JSON format
    jobs_json = json.dumps(job_listings)
    
    # Close the driver
    driver.quit()

    # Return the job listings in JSON format
    return jobs_json

if __name__ == "__main__":
    html_file = sys.argv[1]
    print(scrape_job_listings(html_file))