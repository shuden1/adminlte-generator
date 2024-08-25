from bs4 import BeautifulSoup
from selenium import webdriver
import os
from dotenv import load_dotenv

load_dotenv()
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import threading
import sys
import json

# STEP 1: Find exact selectors
# Based on the provided HTML structure, the job opening blocks are in <div> elements with class 'opening'.
# The job titles and associated URLs are within <a> tags within these blocks.
# Define the selector for job opening blocks
job_opening_block_selector = "div.opening"
# Define the selector for job titles and URLs within those blocks
job_title_and_url_selector = "a"

# STEP 2: Create a Python + Selenium script
def scrape_job_listings(html_file_path):
    service = Service(executable_path=r""+os.getenv("CHROME_DRIVER_PATH")+"")
    profile_folder_path = f"{os.getenv("CHROME_PROFILE_PATH")}{os.path.sep}{str(threading.get_ident())}"
    options = webdriver.ChromeOptions()
    options.add_argument(f"user-data-dir={profile_folder_path}")
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")

    driver = webdriver.Chrome(service=service, options=options)

    # Open the local HTML file
    driver.get(f"file:///{html_file_path}")

    # Scrape all job listings using the previously defined selectors
    job_listings = []
    openings = driver.find_elements(By.CSS_SELECTOR, job_opening_block_selector)
    for opening in openings:
        title_element = opening.find_element(By.CSS_SELECTOR, job_title_and_url_selector)
        job_title = title_element.text.strip()
        job_url = title_element.get_attribute('href').strip()
        job_listings.append({"Job-title": job_title, "URL": job_url})

    driver.quit()

    return json.dumps(job_listings)

# The HTML file path is provided as the first argument to the script
if __name__ == "__main__":
    html_file_path = sys.argv[1]
    print(scrape_job_listings(html_file_path))
