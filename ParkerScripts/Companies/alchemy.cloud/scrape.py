from selenium import webdriver
from selenium.webdriver.common.by import By
import json
import sys

# Check if there is exactly one argument passed (the script name is the first by default)
if len(sys.argv) != 2:
    print("Please provide the target HTML file as an argument.")
    sys.exit(1)

# The target HTML file name received as an argument
target_html_file = sys.argv[1]

# Initialize the WebDriver
driver = webdriver.Chrome()

# Open the HTML file using the WebDriver
driver.get(f"file://{target_html_file}")

# Define the selectors based on the identified blocks and job details from Step 1
job_block_selector = ".collection-item-2.w-dyn-item .careers_block"
job_title_selector = ".job-title"
job_url_selector = ".div-block-56 a"

# Find all job blocks
job_blocks = driver.find_elements(By.CSS_SELECTOR, job_block_selector)

# Initialize a list to hold job details
job_listings = []

# Extract job titles and URLs
for job_block in job_blocks:
    job_title = job_block.find_element(By.CSS_SELECTOR, job_title_selector).text
    job_url = job_block.find_element(By.CSS_SELECTOR, job_url_selector).get_attribute('href')
    job_listings.append({"Job-title": job_title, "URL": job_url})

# Print job listings in JSON format
print(json.dumps(job_listings))

# Close the WebDriver
driver.quit()