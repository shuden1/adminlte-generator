import sys
from bs4 import BeautifulSoup
from selenium import webdriver
import os
from dotenv import load_dotenv

load_dotenv()
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
import threading
import shutil
import json

# STEP 2: Scraper code
def scrape_job_listings(html_file):
    # Read the HTML file
    with open(html_file, 'r', encoding='utf-8') as file:
        html_content = file.read()

    # Parse HTML file with BeautifulSoup
    soup = BeautifulSoup(html_content, 'html.parser')

    # STEP 1: Selectors identified in BeautifulSoup analysis
    job_blocks_selector = ".careers-listing-table"
    job_titles_selector = ".lg-min\\:grid-cols-10 .col-span-6 strong"
    job_urls_selector = ".buttons-wrapper a"

    # Initialize Selenium WebDriver
    profile_folder_path = os.getenv("CHROME_PROFILE_PATH") + os.path.sep + str(threading.get_ident())

    # Chrome service
    service = ChromeService(executable_path=r""+os.getenv("CHROME_DRIVER_PATH")+"")

    # Chrome options
    options = webdriver.ChromeOptions()
    options.add_argument(f"user-data-dir={profile_folder_path}")
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")

    # Start headless browser
    driver = webdriver.Chrome(service=service, options=options)

    driver.get(f"file://{html_file}")

    # Find job blocks
    job_blocks = driver.find_elements(By.CSS_SELECTOR, job_blocks_selector)

    # Create a list to store all job listings information
    job_listings = []

    for job_block in job_blocks:
        # Find job titles and associated URLs within each job block
        job_titles = job_block.find_elements(By.CSS_SELECTOR, job_titles_selector)
        job_urls = job_block.find_elements(By.CSS_SELECTOR, job_urls_selector)

        for title, url in zip(job_titles, job_urls):
            job_listings.append({"Job-title": title.text, "URL": url.get_attribute('href')})

    # Close the driver
    driver.quit()

    # Remove the user profile folder


    # Return job listings as JSON
    return json.dumps(job_listings)

# Read the target HTML file name from the command line argument
target_html_file = sys.argv[1]

print(scrape_job_listings(target_html_file))
