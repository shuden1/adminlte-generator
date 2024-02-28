from selenium import webdriver
from selenium.webdriver.common.by import By
import json
import sys

# Selectors from STEP 1
job_block_selector = ".elementor-element.elementor-element-2b45179"
job_title_selector = ".elementor-element.elementor-element-cfffd87 .elementor-heading-title"
job_url_selector = ".elementor-element.elementor-element-7d7b5ff"

# Read the target HTML file from argument
target_html_filename = sys.argv[1]

# Set up the Selenium WebDriver
driver = webdriver.Chrome()
driver.get(f"file://{target_html_filename}")

# Find all job blocks using the defined selectors
job_blocks = driver.find_elements(By.CSS_SELECTOR, job_block_selector)

# Scrape the job listings
job_listings = [
    {
        "Job-title": job_block.find_element(By.CSS_SELECTOR, job_title_selector).text,
        "URL": job_block.find_element(By.CSS_SELECTOR, job_url_selector).get_attribute("href"),
    }
    for job_block in job_blocks
]

# Close the WebDriver
driver.quit()

# Return the JSON result
print(json.dumps(job_listings))