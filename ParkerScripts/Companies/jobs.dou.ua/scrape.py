import sys
from selenium import webdriver
import os
from dotenv import load_dotenv

load_dotenv()
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
import json
import threading

# STEP 1 Outputs used here for reference when writing the code
job_list_selector = ".l-items"
job_title_and_url_selector = ".title a"

def scrape_job_listings(file_name):
    # Setting up the driver
    profile_folder_path = os.getenv("CHROME_PROFILE_PATH") + os.path.sep + str(threading.get_ident())
    service = ChromeService(executable_path=r""+os.getenv("CHROME_DRIVER_PATH")+"")
    options = webdriver.ChromeOptions()
    options.add_argument(f"user-data-dir={profile_folder_path}")
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")

    # Initialize WebDriver
    driver = webdriver.Chrome(service=service, options=options)

    # Open the local HTML file
    driver.get(f"file:///{file_name}")

    # Find all job listings
    job_elements = driver.find_elements(By.CSS_SELECTOR, job_list_selector + " " + job_title_and_url_selector)  # Combining selectors for precision

    jobs = []
    for job_element in job_elements:
        job_title = job_element.text
        job_url = job_element.get_attribute('href')
        jobs.append({"Job-title": job_title, "URL": job_url})

    driver.quit()

    return json.dumps(jobs)

if __name__ == "__main__":
    filename = sys.argv[1]  # Take the filename from the command-line argument
    print(scrape_job_listings(filename))
