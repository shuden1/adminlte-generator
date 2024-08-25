import sys
import json
import shutil
import threading
from selenium import webdriver
import os
from dotenv import load_dotenv

load_dotenv()
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService

# STEP 2: Selenium script to scrape job listings

def scrape_job_listings(html_file):
    # Initialising headless webdriver
    profile_folder_path = os.getenv("CHROME_PROFILE_PATH") + os.path.sep + str(threading.get_ident())
    service = ChromeService(executable_path=r""+os.getenv("CHROME_DRIVER_PATH")+"")
    options = webdriver.ChromeOptions()
    options.add_argument(f"user-data-dir={profile_folder_path}")
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")

    # Create a new instance of the Chrome driver
    driver = webdriver.Chrome(service=service, options=options)

    # Open the HTML file
    driver.get(f"file:///{html_file}")

    # Scrape all job listings based on provided selectors
    job_opening_elements = driver.find_elements(By.CSS_SELECTOR, '.opening a[data-mapped="true"]')

    # Extract job titles and URLs
    job_listings = []
    for job_element in job_opening_elements:
        job_title = job_element.text
        job_url = job_element.get_attribute('href')
        job_listings.append({"Job-title": job_title, "URL": job_url})

    # Close the driver
    driver.quit()

    # Remove the profile folder


    return json.dumps(job_listings)

if __name__ == "__main__":
    # The target HTML file name should be an argument sent from an external source through the console command
    html_file_name = sys.argv[1]
    result = scrape_job_listings(html_file_name)
    print(result)
