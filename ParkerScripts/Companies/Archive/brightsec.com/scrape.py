from selenium import webdriver
import os
from dotenv import load_dotenv

load_dotenv()
from selenium.webdriver.common.by import By
import json
import sys

# The target HTML file name is provided as a command-line argument
target_html_file = sys.argv[1]

# Create a new instance of the Chrome WebDriver
driver = webdriver.Chrome()

# Open the target HTML file using the file:// protocol
driver.get(f"file:///{target_html_file}")

# Selectors obtained from BeautifulSoup analysis
job_posts_selector = 'div.single_job_post'
job_title_selector = 'span'

# Scrape all job listings
job_listings = []
try:
    job_blocks = driver.find_elements(By.CSS_SELECTOR, job_posts_selector)
    for block in job_blocks:
        anchor = block.find_element(By.XPATH, "./ancestor::a")
        job_title = block.find_element(By.CSS_SELECTOR, job_title_selector).text.strip()
        job_url = anchor.get_attribute('href').strip()
        if job_title and job_url:
            job_listings.append({"Job-title": job_title, "URL": job_url})

except Exception as e:
    print(e)

finally:
    # Convert the job listings to JSON and print
    jobs_json = json.dumps(job_listings)
    print(jobs_json)

    # Close the WebDriver
    driver.quit()
