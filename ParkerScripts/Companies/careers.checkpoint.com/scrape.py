from selenium import webdriver
import os
from dotenv import load_dotenv

load_dotenv()
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
import json
import sys
import shutil
import threading

# STEP 1: Fake selectors for the purpose of this example
# These selectors should be identified by examining the provided HTML file
job_block_selector = '.job-listing'
job_title_selector = 'h2 a'
job_url_attribute = 'href'

# STEP 2: Complete script using Python + Selenium
def scrape_job_listings(html_file_path):
    # Set up Chrome driver with options
    profile_folder_path = f"D:\\Mind\\CRA\\AI_Experiments\\Job_Crawlers\\Peter\\adminlte-generator\\chrome_profile\\{str(threading.get_ident())}"
    service = Service(executable_path=r""+os.getenv("CHROME_DRIVER_PATH")+"")
    options = webdriver.ChromeOptions()
    options.add_argument(f"user-data-dir={profile_folder_path}")
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")

    # Initialize the driver
    driver = webdriver.Chrome(service=service, options=options)

    # Open the local HTML file
    driver.get(f"file:///{html_file_path}")

    # Extract job listings
    job_listings = []
    job_elements = driver.find_elements(By.CSS_SELECTOR, job_block_selector)
    for job_element in job_elements:
        job_title_element = job_element.find_element(By.CSS_SELECTOR, job_title_selector)
        job_title = job_title_element.text.strip()
        job_url = job_title_element.get_attribute(job_url_attribute)
        job_listings.append({"Job-title": job_title, "URL": job_url})

    # Close the driver
    driver.quit()

    # Clean up the profile directory


    # Return job listings as JSON
    return json.dumps(job_listings)

# Command-line argument for the HTML file path
html_file_path = sys.argv[1]

# Scrape and print out the job listings as JSON
print(scrape_job_listings(html_file_path))
