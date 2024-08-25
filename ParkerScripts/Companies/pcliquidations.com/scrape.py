from bs4 import BeautifulSoup
from selenium import webdriver
import os
from dotenv import load_dotenv

load_dotenv()
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import threading
import shutil
import sys
import json

def scrape_job_listings(html_file_path):
    # Step 1: Parsing HTML file with BeautifulSoup
    with open(html_file_path, 'r') as file:
        soup = BeautifulSoup(file.read(), 'html.parser')
    job_blocks_selector = '.pclCareerB'
    job_title_selector = 'h2 a'
    job_url_selector = 'h2 a'

    # Step 2: Selenium script
    profile_folder_path = os.getenv("CHROME_PROFILE_PATH") + os.path.sep + str(threading.get_ident())
    service = Service(executable_path=r""+os.getenv("CHROME_DRIVER_PATH")+"")
    options = webdriver.ChromeOptions()
    options.add_argument(f"user-data-dir={profile_folder_path}")
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")

    driver = webdriver.Chrome(service=service, options=options)

    # Go to the HTML file path passed as an argument
    driver.get(f'file://{html_file_path}')

    # Extract job listings using the defined selectors
    job_listings = []
    job_blocks = driver.find_elements(By.CSS_SELECTOR, job_blocks_selector)

    for job_block in job_blocks:
        title_element = job_block.find_element(By.CSS_SELECTOR, job_title_selector)
        job_title = title_element.text
        job_url = title_element.get_attribute('href')

        job_listings.append({"Job-title": job_title, "URL": job_url})

    # Return the result as JSON
    result = json.dumps(job_listings)

    driver.quit()

    # Remove the profile folder


    return result

if __name__ == "__main__":
    html_file = sys.argv[1]
    print(scrape_job_listings(html_file))
