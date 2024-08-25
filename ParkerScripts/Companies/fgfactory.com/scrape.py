import sys
from selenium import webdriver
import os
from dotenv import load_dotenv

load_dotenv()
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
import threading
import json

def scrape_job_openings(html_file):
    # Set up Chrome options
    profile_folder_path = os.getenv("CHROME_PROFILE_PATH") + "\\" + str(threading.get_ident())
    options = webdriver.ChromeOptions()
    options.add_argument(f"user-data-dir={profile_folder_path}")
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")

    # Set up Chrome driver
    service = ChromeService(executable_path=r""+os.getenv("CHROME_DRIVER_PATH")+"")
    driver = webdriver.Chrome(service=service, options=options)

    # Open the target HTML file
    driver.get(f"file:///{html_file}")

    # Scrape job listings
    job_listings = []
    elements = driver.find_elements(By.CSS_SELECTOR, ".vacancy-box .vacancy-row")

    for element in elements:
        job_title_element = element.find_element(By.CSS_SELECTOR, ".vacancy-title")
        job_url_element = element.find_element(By.CSS_SELECTOR, ".vacancy-view a")
        job_listings.append({
            "Job-title": job_title_element.text,
            "URL": job_url_element.get_attribute('href')
        })

    driver.quit()

    return json.dumps(job_listings)

if __name__ == '__main__':
    html_file = sys.argv[1]
    print(scrape_job_openings(html_file))
