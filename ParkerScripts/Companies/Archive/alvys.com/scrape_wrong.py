from selenium import webdriver
import os
from dotenv import load_dotenv

load_dotenv()
from selenium.webdriver.common.by import By
import sys
import json

def scrape_jobs(html_file_path):
    # Set up Chrome options for headless browsing
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")

    # Use the Chrome WebDriver with options
    with webdriver.Chrome(options=options) as driver:
        driver.get(f"file:///{html_file_path}")

        # Selector for the job blocks considering both job titles and URLs are contained within the same parent element
        job_block_selector = ".elementor-widget-wrap"
        # Selector for the job titles using the class that contains job title text
        job_title_selector = "h2"
        # Selector for the URL which is always contained within an 'a' element within the job block
        job_url_selector = "a"

        # Find job blocks
        job_blocks = driver.find_elements(By.CSS_SELECTOR, job_block_selector)
        job_listings = []

        for job_block in job_blocks:
            # Extract the job title and URL from each block
            title_elements = job_block.find_elements(By.CSS_SELECTOR, job_title_selector)
            url_elements = job_block.find_elements(By.CSS_SELECTOR, job_url_selector)

            # Ensure we are capturing the correct pairs of titles and URLs
            for title_element, url_element in zip(title_elements, url_elements):
                # Add title and URL to the job_listings if they're not empty
                title_text = title_element.text.strip()
                url = url_element.get_attribute('href').strip()
                if title_text and url:
                    job_listings.append({"Job-title": title_text, "URL": url})

        return json.dumps(job_listings)

# Script execution starts here
if __name__ == "__main__":
    html_file_arg = sys.argv[1]  # The HTML file path is passed as the first argument
    print(scrape_jobs(html_file_arg))
