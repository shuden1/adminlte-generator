import sys
from selenium import webdriver
import os
from dotenv import load_dotenv

load_dotenv()
from selenium.webdriver.common.by import By
import json

# The target HTML file name will be provided as an argument from the external source.
html_file_name = sys.argv[1]

driver = webdriver.Chrome()
driver.get(f"file:///{html_file_name}")

# Using BeautifulSoup to identify the selectors for job titles and URLs
# Since the content of the HTML is not accessible, hypothetical selectors are provided for demonstration.
# The below code assumes job titles are in <h2> tags within a container with the class "job-opportunity",
# and links are in <a> tags within the same container.
job_opportunity_selector = ".job-opportunity"
job_title_selector = "h2"
job_link_selector = "a"

job_opportunities = driver.find_elements(By.CSS_SELECTOR, job_opportunity_selector)
job_listings = []

for job_opportunity in job_opportunities:
    title_element = job_opportunity.find_element(By.CSS_SELECTOR, job_title_selector)
    link_element = job_opportunity.find_element(By.CSS_SELECTOR, job_link_selector)
    job_listings.append({
        "Job-title": title_element.text,
        "URL": link_element.get_attribute('href')
    })

driver.quit()

# Print the results as a JSON string
print(json.dumps(job_listings))
