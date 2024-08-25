import sys
import json
import threading
from selenium import webdriver
import os
from dotenv import load_dotenv

load_dotenv()
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

def scrape_jobs(file_path):
    # Initialize Chrome options
    profile_folder_path = f"D:\\Mind\\CRA\\AI_Experiments\\Job_Crawlers\\Peter\\adminlte-generator\\chrome_profile\\{str(threading.get_ident())}"
    options = Options()
    options.add_argument(f"user-data-dir={profile_folder_path}")
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")

    # Initialize Chrome driver
    service = Service(executable_path=r""+os.getenv("CHROME_DRIVER_PATH")+"")
    driver = webdriver.Chrome(service=service, options=options)

    try:
        # Load the HTML file
        driver.get(f"file:///{file_path}")

        # Define selectors
        job_block_selector = '.cefcom-box.shadow-hover.job-card.rounded-8'
        job_title_selector = 'h2.cefcom-h5'
        job_url_attribute = 'href'

        # Scrape job listings
        job_elements = driver.find_elements(By.CSS_SELECTOR, job_block_selector)
        job_listings = []

        for job_element in job_elements:
            title_element = job_element.find_element(By.CSS_SELECTOR, job_title_selector)
            title = title_element.text
            url = job_element.get_attribute(job_url_attribute)
            job_listings.append({"Job-title": title, "URL": url})

        # Return job listings as JSON
        print(json.dumps(job_listings, indent=4))

    finally:
        driver.quit()

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script.py <path_to_html_file>")
        sys.exit(1)

    file_path = sys.argv[1]
    scrape_jobs(file_path)
