from selenium import webdriver
import os
from dotenv import load_dotenv

load_dotenv()
from selenium.webdriver.common.by import By
import json
import sys

def scrape_jobs(driver, job_container_selector, job_title_selector, job_link_selector):
    # Find job containers
    job_containers = driver.find_elements(By.CSS_SELECTOR, job_container_selector)

    # List to hold job data
    job_listings = []
    for container in job_containers:
        # Find titles and links within the container
        titles = container.find_elements(By.CSS_SELECTOR, job_title_selector)
        links = container.find_elements(By.CSS_SELECTOR, job_link_selector)

        # Extract text and href
        for title, link in zip(titles, links):
            if link.get_attribute('href'):
                job_listings.append({
                    'Job-title': title.text,
                    'URL': link.get_attribute('href')
                })

    return job_listings

# Arguments from the external source
html_file_path = sys.argv[1]

# ChromeDriver setup options
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--disable-gpu')
chrome_options.add_argument('--no-sandbox')

# Selectors for job titles and links
job_container_selector = '.elementor-widget-container'
job_title_selector = 'span.pafe-table-body-first-text'
job_link_selector = 'a.pafe-table-body-text[href]'

# Start the WebDriver
driver = webdriver.Chrome(options=chrome_options)

# Load the HTML file
driver.get(f"file:///{html_file_path}")

# Scrape jobs listings
jobs = scrape_jobs(driver, job_container_selector, job_title_selector, job_link_selector)

# Quit the WebDriver
driver.quit()

# Print job listings in JSON format
print(json.dumps(jobs, indent=4))
