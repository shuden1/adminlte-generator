from selenium import webdriver
import os
from dotenv import load_dotenv

load_dotenv()
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import sys
import json

# Read the file name from the command-line argument
html_file_name = sys.argv[1]

# Initialize the webdriver
driver = webdriver.Chrome()

# Open the HTML file in the browser through the webdriver
driver.get(f"file://{html_file_name}")

# Identifying the HTML block selectors for Job Openings and the selectors for job titles
job_block_selector = "div.div-block-109"
job_title_selector = "h1.heading-286"

# Wait until the job titles are available in the DOM or timeout after 10 seconds
WebDriverWait(driver, 10).until(
    EC.presence_of_all_elements_located((By.CSS_SELECTOR, job_title_selector))
)

# Scrape all job listings
job_listings = []
job_elements = driver.find_elements(By.CSS_SELECTOR, job_block_selector)

for job_elem in job_elements:
    # Check if job title exists within this job element
    title_elements = job_elem.find_elements(By.CSS_SELECTOR, job_title_selector)
    if title_elements:
        job_title = title_elements[0].text
        # Assuming that job URL is the href attribute of the first 'a' tag inside the job element
        # If no 'a' tag present, URL will be set to 'Not available'
        job_url_elements = job_elem.find_elements(By.CSS_SELECTOR, "a")
        job_url = job_url_elements[0].get_attribute('href') if job_url_elements else 'Not available'
        job_listings.append({"Job-title": job_title, "URL": job_url})

# Output the result in JSON format
print(json.dumps(job_listings))

# Close the webdriver
driver.quit()
