from bs4 import BeautifulSoup
import sys
from selenium import webdriver
import os
from dotenv import load_dotenv

load_dotenv()
from selenium.webdriver.common.by import By
import json

# Load HTML file and parse job openings with BeautifulSoup
html_file = sys.argv[1]
with open(html_file, 'r', encoding='utf-8') as file:
    soup = BeautifulSoup(file, 'html.parser')

job_blocks_selector = '.opening-job.job'
job_title_selector = 'h4.details-title.job-title.link--block-target'
job_url_selector = 'a.link--block.details'

# Prepare Selenium script
def scrape_job_listings():
    driver = webdriver.Chrome()
    driver.get(f'file:///{html_file}')

    job_blocks = driver.find_elements(By.CSS_SELECTOR, job_blocks_selector)
    job_listings = []

    for job_block in job_blocks:
        title_element = job_block.find_element(By.CSS_SELECTOR, job_title_selector)
        url_element = job_block.find_element(By.CSS_SELECTOR, job_url_selector)

        job_listings.append({"Job-title": title_element.text, "URL": url_element.get_attribute('href')})

    driver.quit()

    return json.dumps(job_listings)


# Call the function and print the result
if __name__ == "__main__":
    print(scrape_job_listings())
