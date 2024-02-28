from selenium import webdriver
from selenium.webdriver.common.by import By
import json
import sys

# The target HTML file's name is provided as a command line argument.
html_file_name = sys.argv[1]

# Initialization of ChromeDriver.
driver = webdriver.Chrome()
driver.get(f"file:///{html_file_name}")

# Define a JSON structure to hold the scraped data.
scraped_data = []

# Use the BeautifulSoup selectors that were identified earlier.
job_openings_selector = "div.grow ul > li"  # Parent element of job opening blocks
job_title_selector = "a > span"               # Job title is within the <span> tag within <a> tag
job_url_selector = "a"               # Job URL is within the <a> tag

# Find all job listings.
job_listings = driver.find_elements(By.CSS_SELECTOR, job_openings_selector)

# For each job listing, extract the job title and URL.
for listing in job_listings:
    job_title_element = listing.find_element(By.CSS_SELECTOR, job_title_selector)
    job_title = driver.execute_script("return arguments[0].textContent;", job_title_element).strip()
    job_url_element = listing.find_element(By.CSS_SELECTOR, job_url_selector)
    job_url = job_url_element.get_attribute('href')
    scraped_data.append({"Job-title": job_title, "URL": job_url})

# Close the ChromeDriver.
driver.quit()

# Output the result as JSON.
print(json.dumps(scraped_data))
