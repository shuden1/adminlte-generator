import sys
from selenium import webdriver
import os
from dotenv import load_dotenv

load_dotenv()
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
import threading
import json

def scrape_job_listings(file_name):
    # Setup Chrome options
    chrome_options = webdriver.ChromeOptions()
    profile_folder_path = f"{os.getenv("CHROME_PROFILE_PATH")}{os.path.sep}{threading.get_ident()}"
    chrome_options.add_argument(f"user-data-dir={profile_folder_path}")
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")

    # Initialize WebDriver
    service = ChromeService(executable_path=r""+os.getenv("CHROME_DRIVER_PATH")+"")
    driver = webdriver.Chrome(service=service, options=chrome_options)

    # Load the HTML file
    driver.get(f"file:///{file_name}")

    # Selectors from STEP 1
    job_blocks_selector = ".employer-job-listing-single.shadow-sm.bg-white"
    job_title_selector = "h5 a"

    # Collect job listings
    job_listings = []
    job_blocks = driver.find_elements(By.CSS_SELECTOR, job_blocks_selector)
    for block in job_blocks:
        title_element = block.find_element(By.CSS_SELECTOR, job_title_selector)
        job_listings.append({"Job-title": title_element.text, "URL": title_element.get_attribute("href")})

    # Clean up
    driver.quit()

    # Convert the list to JSON and print
    print(json.dumps(job_listings, indent=2))

if __name__ == "__main__":
    scrape_job_listings(sys.argv[1])
