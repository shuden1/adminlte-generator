from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import json

# Define the command-line argument for the HTML file
target_html_file = 'path/to/html'  # Placeholder for the command-line argument

# Set up headless Chrome options
options = Options()
options.headless = True
options.add_argument("--disable-gpu")

# Initialize a new driver with the headless options
driver_service = Service(executable_path='chromedriver')  # Assuming 'chromedriver' is in PATH
driver = webdriver.Chrome(service=driver_service, options=options)

# Open the HTML file in the headless browser
driver.get(f'file:///{target_html_file}')

# Define the selectors for the job opening blocks and job details
jobs_container_selector = ".user-items-list-item-container.user-items-list-simple"
job_title_selector = ".item-title"
job_link_selector = "a"

# Locate job opening blocks and extract the job details
blocks = driver.find_elements(By.CSS_SELECTOR, jobs_container_selector)
job_listings = []
for block in blocks:
    # Locate job titles and URLs within each block
    titles = block.find_elements(By.CSS_SELECTOR, job_title_selector)
    links = block.find_elements(By.CSS_SELECTOR, job_link_selector)
    for title, link in zip(titles, links):
        job_listings.append({
            "Job-title": title.text.strip(),
            "URL": link.get_attribute('href').strip()
        })

# Print the job listings as JSON
print(json.dumps(job_listings))

# Clean up and close the browser
driver.quit()