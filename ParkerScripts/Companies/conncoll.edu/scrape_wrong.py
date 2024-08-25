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
    profile_folder_path = os.getenv("CHROME_PROFILE_PATH") + "\\" + str(threading.get_ident())
    service = Service(executable_path=r""+os.getenv("CHROME_DRIVER_PATH")+"")

    options = Options()
    options.add_argument(f"user-data-dir={profile_folder_path}")
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")

    driver = webdriver.Chrome(service=service, options=options)

    try:
        driver.get(f"file:///{file_path}")

        # Update the selectors based on the analysis
        job_blocks = driver.find_elements(By.CSS_SELECTOR, '.job-opening')  # Replace with actual class or parameter
        job_listings = []

        for job in job_blocks:
            title_element = job.find_element(By.CSS_SELECTOR, 'a')  # Replace with actual class or parameter
            title = title_element.text
            url = title_element.get_attribute('href')
            job_listings.append({"Job-title": title, "URL": url})

        print(json.dumps(job_listings, indent=4))

    finally:
        driver.quit()

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script.py <path_to_html_file>")
        sys.exit(1)

    file_path = sys.argv[1]
    scrape_jobs(file_path)
