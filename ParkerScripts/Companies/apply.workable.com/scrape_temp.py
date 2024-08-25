from selenium import webdriver
import os
from dotenv import load_dotenv

load_dotenv()
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import json
import threading
import sys

# Read the target HTML filename from the command line argument
target_html_file = sys.argv[1]

# Selectors for STEP 1
job_block_selector = "ul.styles--Qqz1P > li.styles--1vo9F"
job_title_selector = "h3.styles--3TJHk > span"
job_url_selector = "h3.styles--3TJHk"  # Assuming URLs are in some attribute of the h3 element

def scrape_job_listings(file_path):
    # Set up Chrome driver options
    options = Options()
    profile_folder_path = os.getenv("CHROME_PROFILE_PATH") + "\\" + str(threading.get_ident())
    options.add_argument(f"user-data-dir={profile_folder_path}")
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")

    # Set up Chrome service
    service = ChromeService(executable_path=r""+os.getenv("CHROME_DRIVER_PATH")+"")

    # Initialize the driver
    driver = webdriver.Chrome(service=service, options=options)

    # Open the target HTML file
    driver.get(f"file://{file_path}")

    # Scrape job listings
    job_listings = []
    job_blocks = driver.find_elements(By.CSS_SELECTOR, job_block_selector)
    for job_block in job_blocks:
        job_title_elem = job_block.find_element(By.CSS_SELECTOR, job_title_selector)
        job_title = job_title_elem.text.strip()

        # Assuming the job URL is in some attribute of the h3 element
        job_url = job_block.find_element(By.CSS_SELECTOR, job_url_selector).get_attribute('some_attribute')

        job_listings.append({"Job-title": job_title, "URL": job_url})

    driver.quit()

    return json.dumps(job_listings)

# Call the function with the target HTML file as the argument
print(scrape_job_listings(target_html_file))
