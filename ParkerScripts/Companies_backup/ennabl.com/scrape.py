import sys
from selenium import webdriver
from selenium.webdriver.common.by import By
import json

# Argument from the external source
html_file_name = sys.argv[1]  # The HTML file name is provided as a command-line argument

# Selenium script to scrape job listings
driver = webdriver.Chrome()
driver.get(f"file:///{html_file_name}")

# Using the exact selectors defined from BeautifulSoup analysis
job_blocks = driver.find_elements(By.CSS_SELECTOR, ".work-list .paddind-section-little p")
jobs_json = []

for job_block in job_blocks:
    url_element = job_block.find_element(By.CSS_SELECTOR, "a")
    job_title = url_element.text.strip()
    job_url = url_element.get_attribute("href").strip()
    jobs_json.append({"Job-title": job_title, "URL": job_url})

# Close the driver after the operation is complete
driver.quit()

# Return the scraped job listings as JSON
print(json.dumps(jobs_json))