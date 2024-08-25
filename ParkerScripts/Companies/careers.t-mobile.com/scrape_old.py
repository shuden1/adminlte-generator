from selenium import webdriver
import os
from dotenv import load_dotenv

load_dotenv()
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
import shutil
import threading
import sys
import json

def scrape_job_listings(html_file_path):
    # Setup a headless ChromeDriver with specified options
    service = ChromeService(executable_path=r""+os.getenv("CHROME_DRIVER_PATH")+"")
    thread_id = threading.get_ident()
    profile_folder_path = os.getenv("CHROME_PROFILE_PATH") + "\\" + str(thread_id)
    options = webdriver.ChromeOptions()
    options.add_argument(f"user-data-dir={profile_folder_path}")
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")

    # Initialize the driver
    driver = webdriver.Chrome(service=service, options=options)

    # Open the HTML file in headless browser
    driver.get("file:///" + html_file_path)

    # Using the defined selectors to scrape job listings
    job_selector = '.job-innerwrap'  # Block with Job Openings
    title_selector = '.jobTitle a'   # job titles and their associated URLs

    jobs_data = []

    job_elements = driver.find_elements(By.CSS_SELECTOR, job_selector)
    for job_element in job_elements:
        title_element = job_element.find_element(By.CSS_SELECTOR, title_selector)
        jobs_data.append({
            "Job-title": title_element.text.split("  ")[0].strip(),
            "URL": title_element.get_attribute('href')
        })

    # Close the driver
    driver.quit()

    # Remove the profile folder
    # shutil.rmtree(profile_folder_path, ignore_errors=True)

    # Return the JSON result
    return json.dumps(jobs_data)

if __name__ == "__main__":
    # the target HTML file name is an argument sent from an external source
    html_file_path = sys.argv[1]
    result = scrape_job_listings(html_file_path)
    print(result)
