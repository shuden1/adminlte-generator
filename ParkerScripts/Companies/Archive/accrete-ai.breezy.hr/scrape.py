from bs4 import BeautifulSoup
from selenium import webdriver
import os
from dotenv import load_dotenv

load_dotenv()
from selenium.webdriver.common.by import By
import sys
import json

if len(sys.argv) == 2:
    html_file_path = sys.argv[1]
    options = webdriver.ChromeOptions()
    options.add_argument("headless")
    driver = webdriver.Chrome(options=options)
    driver.get(f"file://{html_file_path}")

    job_blocks_selector = '.positions.location .position'
    job_title_selector = 'h2'
    job_url_selector = 'a'

    job_blocks = driver.find_elements(By.CSS_SELECTOR, job_blocks_selector)
    job_listings = []

    for job_block in job_blocks:
        job_title_element = job_block.find_element(By.CSS_SELECTOR, job_title_selector)
        job_title = job_title_element.text.strip()

        job_url_element = job_block.find_element(By.CSS_SELECTOR, job_url_selector)
        job_url = job_url_element.get_attribute('href').strip()

        job_listings.append({"Job-title": job_title, "URL": job_url})

    driver.quit()

    print(json.dumps(job_listings))
else:
    print("Invalid number of arguments. Please provide the HTML file path as the only argument.")
