from selenium import webdriver
from selenium.webdriver.common.by import By
import json
import sys

# Set up the selectors for job opening blocks and job titles/URLs
job_openings_selector = ".block .job-opening"
job_title_and_url_selector = "h3 a"

# The name of the HTML file should be passed as an argument from an external source
html_file = sys.argv[1]

# Initialize Selenium WebDriver for Chrome
driver = webdriver.Chrome()

# Open the local HTML file
driver.get(f"file:///{html_file}")

# Scrape job opening information
jobs_data = []
job_openings = driver.find_elements(By.CSS_SELECTOR, job_openings_selector)

for job_opening in job_openings:
    # Find the job title and URL within the job opening block
    title_element = job_opening.find_element(By.CSS_SELECTOR, job_title_and_url_selector)
    job_title = title_element.text
    job_url = title_element.get_attribute('href')
    jobs_data.append({"Job-title": job_title, "URL": job_url})

# Return scraped data as JSON
print(json.dumps(jobs_data))

# Quit the WebDriver session
driver.quit()