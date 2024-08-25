from selenium import webdriver
import os
from dotenv import load_dotenv

load_dotenv()
import json
import sys

# Extract the HTML file name from the input argument
html_file = sys.argv[1]

# Selectors defined from the BeautifulSoup analysis
job_offers_section_selector = '.job-offers-section'
job_title_selector = 'h4[data-job-offers-element="title"]'
job_url_selector = 'a[href]'

# Start the Selenium WebDriver
driver = webdriver.Chrome()

# Open the local HTML file with the WebDriver
driver.get("file:///{}".format(html_file))

# Initialize the list to store job offers
job_offers = []

# Find job offer sections in the HTML document
job_sections = driver.find_elements_by_css_selector(job_offers_section_selector)

# Loop over each job section and extract the job titles and URLs
for section in job_sections:
    jobs = section.find_elements_by_css_selector(job_title_selector)
    links = section.find_elements_by_css_selector(job_url_selector)

    # Aggregate the titles and URLs into the job_offers list
    for job, link in zip(jobs, links):
        job_offers.append({
            "Job-title": job.text,
            "URL": link.get_attribute('href')
        })

# Return the scraped job offers as JSON and close the Selenium WebDriver
print(json.dumps(job_offers))
driver.quit()
