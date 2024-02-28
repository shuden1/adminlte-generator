from selenium import webdriver
from selenium.webdriver.common.by import By
import json
import sys

# Get the html filename from the command line argument
html_file_name = sys.argv[1]

# Start the Chrome session
driver = webdriver.Chrome()

# Open the local HTML file
driver.get(f"file://{html_file_name}")

# Define the selectors based on BeautifulSoup analysis
job_block_selector = ".elementor-post.elementor-grid-item.ecs-post-loop"
job_title_and_url_selector = ".elementor-post.elementor-grid-item.ecs-post-loop .elementor-heading-title a"

# Scrape all job listings
job_elements = driver.find_elements(By.CSS_SELECTOR, job_title_and_url_selector)
job_listings = []
for job_element in job_elements:
    title = job_element.text.strip()
    url = job_element.get_attribute('href').strip()
    if url.startswith("https://concentric.ai/hiring/"):
        job_listings.append({"Job-title": title, "URL": url})

# Output result in JSON format
output = json.dumps(job_listings)
print(output)

# Close the browser
driver.quit()