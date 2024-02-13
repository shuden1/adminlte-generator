from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
import json
import sys

# STEP 2: Scrape job listings using Selenium

# The target HTML file name is provided as a command-line argument
html_file_name = sys.argv[1]

# Initialize Selenium WebDriver
service = ChromeService(executable_path=ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)

# Defining the BeautifulSoup selector based on the file analysis
job_openings_selector = '.c-2x2'  # Job opening blocks have the class 'c-2x2'
job_title_selector = 'h3'  # Job title is in an 'h3' tag within the job opening block
job_link_selector = 'a'  # The 'a' tag contains the URL for the job

# Open the local HTML file using Selenium
driver.get(f"file:///{html_file_name}")

# Scrape job listings
job_listings = []
job_blocks = driver.find_elements(By.CSS_SELECTOR, job_openings_selector)

for block in job_blocks:
    title_element = block.find_element(By.CSS_SELECTOR, job_title_selector)
    job_title = title_element.text
    link_element = block.find_element(By.CSS_SELECTOR, job_link_selector)
    job_url = link_element.get_attribute('href')
    job_listings.append({'Job-title': job_title, 'URL': job_url})

# Output the scraped data in JSON format
jobs_json = json.dumps(job_listings)

# Print the JSON result to standard output
print(jobs_json)

# Close the WebDriver session
driver.quit()