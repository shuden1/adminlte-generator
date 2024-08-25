import sys
from bs4 import BeautifulSoup
from selenium import webdriver
import os
from dotenv import load_dotenv

load_dotenv()
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import threading
import shutil
import json

# STEP 1: Selectors
# Job Opening blocks selector: .card
# Job Title selector: .card-header h3 button
# Job URL selector: .btn.btn-link (Since there is no actual URL, just use data-target attribute as URL)

# Proceed to STEP 2
if len(sys.argv) > 1:
    file_name = sys.argv[1]

    # Setting up the headless ChromeDriver with specified options
    profile_folder_path = os.getenv("CHROME_PROFILE_PATH") + "\\" + str(threading.get_ident())
    service = Service(executable_path=r""+os.getenv("CHROME_DRIVER_PATH")+"")
    options = webdriver.ChromeOptions()
    options.add_argument(f"user-data-dir={profile_folder_path}")
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")

    # Start the browser with the selenium service and options
    driver = webdriver.Chrome(service=service, options=options)

    try:
        # Open the file with driver
        driver.get(f"file:///{file_name}")

        # Scrape job listings
        job_listings = []
        job_blocks = driver.find_elements(By.CSS_SELECTOR, ".card")
        for job_block in job_blocks:
            title_element = job_block.find_element(By.CSS_SELECTOR, ".card-header h3 button")
            job_title = title_element.get_attribute('textContent').strip()
            job_url = title_element.get_attribute('data-target')
            job_listings.append({"Job-title": job_title, "URL": job_url})

        # Return the JSON result
        print(json.dumps(job_listings))

    finally:
        driver.quit()
