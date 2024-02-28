from selenium import webdriver
from selenium.webdriver.common.by import By
import json
import sys

# Get the target HTML file name from command line argument
html_file_name = sys.argv[1]

# Initialize the Chrome WebDriver
driver = webdriver.Chrome()

# Open the local HTML file (relative path)
driver.get(f"file:///{html_file_name}")

# Locators defined based on the provided HTML structure
job_opening_selector = ".elementor-toggle-item"
job_title_selector = ".elementor-toggle-title"
job_url_attribute = "href"

# Find job listings using the selectors
job_openings = driver.find_elements(By.CSS_SELECTOR, job_opening_selector)

# Scrape job titles and URLs
jobs_list = []
for job in job_openings:
    title_element = job.find_element(By.CSS_SELECTOR, job_title_selector)
    title = title_element.text
    url = title_element.get_attribute(job_url_attribute)
    # Check if URL is empty and try to find a URL in the job description section
    if not url:
        description_section = job.find_element(By.CSS_SELECTOR, '.elementor-tab-content')
        url_elements = description_section.find_elements(By.TAG_NAME, 'a')
        for elem in url_elements:
            href = elem.get_attribute(job_url_attribute)
            if href.startswith("mailto:"):
                url = href
                break
    jobs_list.append({'Job-title': title, 'URL': url})

# Convert the list of job listings to JSON
json_output = json.dumps(jobs_list)

# Close the driver
driver.quit()

# Output the JSON string
print(json_output)