from selenium import webdriver
import os
from dotenv import load_dotenv

load_dotenv()
from selenium.webdriver.common.by import By
import json
import sys

# The target HTML file name should be an argument sent from an external source
html_file_path = sys.argv[1]

# Initialize the WebDriver
driver = webdriver.Chrome()

# Open the HTML file
driver.get(f"file://{html_file_path}")

# Selectors identified in Step 1
job_block_selector = ".card.card--career"
job_title_selector = "h1.card__heading.heading--4"
job_url_selector = ".card__link"

# Find all job listings using selectors from Step 1
job_elements = driver.find_elements(By.CSS_SELECTOR, job_block_selector)
job_listings = []

# Extract job titles and URLs from the job elements
for job_element in job_elements:
    title_element = job_element.find_element(By.CSS_SELECTOR, job_title_selector)
    url_element = job_element.find_element(By.CSS_SELECTOR, job_url_selector)

    job_title = title_element.text.strip()
    job_url = url_element.get_attribute("href").strip()

    job_listings.append({"Job-title": job_title, "URL": job_url})

# Output the job listings as JSON
print(json.dumps(job_listings))

# Close the driver
driver.quit()
