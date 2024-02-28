from selenium import webdriver
from selenium.webdriver.common.by import By
import json
import sys

# The target HTML file name should be an argument sent from an external source
html_file = sys.argv[1]

# Set up the Chrome driver
driver = webdriver.Chrome()

# Load the HTML file
driver.get(f"file:///{html_file}")

# Use the selectors identified in Step 1 to scrape job listings
job_opening_block_selector = ".notion-list-view .notion-selectable.notion-page-block.notion-collection-item"
job_title_selector = "div[style*='min-width: 240px']"
job_url_selector = "a[href]"
results = []

# Find job opening blocks
blocks = driver.find_elements(By.CSS_SELECTOR, job_opening_block_selector)
for block in blocks:
    title_elem = block.find_element(By.CSS_SELECTOR, job_title_selector)
    job_title = title_elem.text.strip() if title_elem else ""
    link_elem = block.find_element(By.CSS_SELECTOR, job_url_selector)
    job_url = link_elem.get_attribute('href').strip() if link_elem else ""
    results.append({"Job-title": job_title, "URL": job_url})

# Output the result as JSON
print(json.dumps(results))

# Close the driver
driver.quit()