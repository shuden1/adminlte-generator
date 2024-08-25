from selenium import webdriver
import os
from dotenv import load_dotenv

load_dotenv()
from selenium.webdriver.common.by import By
import json
import sys

# Check if the argument is provided
if len(sys.argv) < 2:
    raise Exception('HTML file name argument is missing')

# Assigning the filename to a variable
file_name = sys.argv[1]

# Initialize the Chrome driver
driver = webdriver.Chrome()

# Open the local HTML file
driver.get(f"file:///{file_name}")

# Selectors defined in Step 1
job_opening_block_selector = ".t650__container.t-card__container.t-container"
job_title_selector = ".t-card__title.t-name.t-name_lg.t650__bottommargin"

# Find the job openings elements
job_opening_blocks = driver.find_elements(By.CSS_SELECTOR, job_opening_block_selector)

# Store the results
job_listings = []

# Loop through each opening and extract the required information
for block in job_opening_blocks:
    titles = block.find_elements(By.CSS_SELECTOR, job_title_selector)
    for title in titles:
        job_title = title.text.strip()
        url = title.find_element(By.TAG_NAME, 'a').get_attribute('href')
        job_listings.append({"Job-title": job_title, "URL": url})

# Close the driver
driver.quit()

# Output the job listings as JSON
print(json.dumps(job_listings))
