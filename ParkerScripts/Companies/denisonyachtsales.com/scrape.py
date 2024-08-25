import sys
import json
import threading
from selenium import webdriver
import os
from dotenv import load_dotenv

load_dotenv()
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

def main():
    # Get the target HTML file name from the command line argument
    target_html_file = sys.argv[1]

    # Profile folder path
    profile_folder_path = os.getenv("CHROME_PROFILE_PATH") + os.path.sep + str(threading.get_ident())

    # Set up Chrome options
    options = Options()
    options.add_argument(f"user-data-dir={profile_folder_path}")
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")

    # Set up Chrome service
    service = Service(executable_path=r""+os.getenv("CHROME_DRIVER_PATH")+"")

    # Initialize the WebDriver
    driver = webdriver.Chrome(service=service, options=options)

    # Load the target HTML file
    driver.get(f"file:///{target_html_file}")

    # Define the selectors for job listings
    job_listing_selector = "div.inn_content_bottom_boxes"
    job_title_selector = "h4"
    job_url_selector = "a.details"

    # Find all job listings
    job_listings = driver.find_elements(By.CSS_SELECTOR, job_listing_selector)

    # Extract job titles and URLs
    jobs = []
    for job in job_listings:
        job_title_element = job.find_element(By.CSS_SELECTOR, job_title_selector)
        job_url_element = job.find_element(By.CSS_SELECTOR, job_url_selector)
        job_title = job_title_element.text.strip()
        job_url = job_url_element.get_attribute("href")
        jobs.append({"Job-title": job_title, "URL": job_url})

    # Close the WebDriver
    driver.quit()

    # Print the JSON result
    print(json.dumps(jobs, indent=4))

if __name__ == "__main__":
    main()
