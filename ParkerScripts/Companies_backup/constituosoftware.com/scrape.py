from selenium import webdriver
from selenium.webdriver.common.by import By
import json
import sys

# The target HTML file name should be an argument sent from an external source through the console command as the single input parameter.
target_html_file = sys.argv[1]

# Initialize the Chrome WebDriver
driver = webdriver.Chrome()
driver.get(f"file://{target_html_file}")

# Selectors for the job openings based on the observed structure of the webpage
job_openings_selector = '.wpb_row.vc_row-fluid.standard-section.section.section-no-parallax.stretch .wpb_text_column.wpb_content_element p a'

# Find all job opening blocks using the defined selectors
job_opening_blocks = driver.find_elements(By.CSS_SELECTOR, job_openings_selector)

# Prepare the list for job details
jobs = []

# Extract job titles and URLs from each job opening block
for block in job_opening_blocks:
    # Find the associated URL in the same block
    job_title = block.text
    job_url = block.get_attribute('href')
    jobs.append({"Job-title": job_title, "URL": job_url})

# Print out the jobs in JSON format (print is used to simulate returning the JSON)
print(json.dumps(jobs))

# Quit the WebDriver
driver.quit()
