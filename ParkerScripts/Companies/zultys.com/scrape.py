from selenium import webdriver
import os
from dotenv import load_dotenv

load_dotenv()
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
import threading
import shutil
import json
import sys

# Extract HTML file name from the external argument
html_file = sys.argv[1]

def scrape_job_listings(html_file):
    # Initialising a headless webdriver with options and service
    profile_folder_path = os.getenv("CHROME_PROFILE_PATH") + os.path.sep + str(threading.get_ident())
    service = ChromeService(executable_path=r""+os.getenv("CHROME_DRIVER_PATH")+"")
    options = webdriver.ChromeOptions()
    options.add_argument(f"user-data-dir={profile_folder_path}")
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    driver = webdriver.Chrome(service=service, options=options)

    # Open the provided HTML file
    driver.get(f"file:///{html_file}")

    # Scraping job listings using selectors from Step 1
    job_blocks_selector = '.elementor-post.elementor-grid-item'
    job_title_selector = 'h2.elementor-post__title > a'
    jobs = []

    job_elements = driver.find_elements(By.CSS_SELECTOR, job_blocks_selector)
    for job_element in job_elements:
        title_element = job_element.find_element(By.CSS_SELECTOR, job_title_selector)
        job_title = title_element.text.strip()
        job_url = title_element.get_attribute('href')
        jobs.append({"Job-title": job_title, "URL": job_url})

    # Closing the webdriver
    driver.quit()

    # Remove the profile folder
    # shutil.rmtree(profile_folder_path, ignore_errors=True)

    # Print the jobs in JSON format
    print(json.dumps(jobs))

# Call the function with the provided HTML file
scrape_job_listings(html_file)
