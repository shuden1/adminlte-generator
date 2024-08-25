from selenium import webdriver
import os
from dotenv import load_dotenv

load_dotenv()
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
import json
import sys
import threading

# STEP 1 results: Job Openings Block Selector and Job Title & URL Selectors
job_openings_block_selector = "div.avail-positions-container ul li"
job_title_selector = "strong"
job_url_selector = "a"

# STEP 2: Python + Selenium script

def scrape_job_listings(html_file_path):
    # Initialize the headless webdriver with options and service
    options = webdriver.ChromeOptions()
    profile_folder_path = f"D:\\Mind\\CRA\\AI_Experiments\\Job_Crawlers\\Peter\\adminlte-generator\\chrome_profile\\{str(threading.get_ident())}"
    options.add_argument(f"user-data-dir={profile_folder_path}")
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    service = ChromeService(executable_path=r""+os.getenv("CHROME_DRIVER_PATH")+"")
    driver = webdriver.Chrome(service=service, options=options)

    # Open the HTML file
    driver.get(f"file://{html_file_path}")

    # Find job listings based on the selectors identified in STEP 1
    job_openings_elements = driver.find_elements(By.CSS_SELECTOR, job_openings_block_selector)

    # Scrape the job titles and URLs
    job_listings = []
    for job_element in job_openings_elements:
        job_title_element = job_element.find_element(By.CSS_SELECTOR, job_title_selector)
        job_url_element = job_element.find_element(By.CSS_SELECTOR, job_url_selector)
        job_title = job_title_element.text.strip()
        job_url = job_url_element.get_attribute('href').strip()
        job_listings.append({"Job-title": job_title, "URL": job_url})

    driver.quit()

    # Return the job listings as JSON
    return json.dumps(job_listings)

if __name__ == "__main__":
    html_file_path = sys.argv[1]
    print(scrape_job_listings(html_file_path))
