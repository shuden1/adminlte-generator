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

def main():
    # Get the HTML file name from the command line argument
    html_file = sys.argv[1]

    # Define the profile folder path
    profile_folder_path = os.getenv("CHROME_PROFILE_PATH") + "\\" + str(threading.get_ident())

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

    # Load the HTML file
    driver.get(f"file:///{html_file}")

    # Define the selectors
    job_opening_selector = "div.list-group-item.list-group-item-action"
    job_title_selector = "span.jd-nav-label"
    job_url_selector = "button.jd-btn"

    # Find all job postings
    job_elements = driver.find_elements(By.CSS_SELECTOR, job_opening_selector)
    job_listings = []

    for job_element in job_elements:
        job_title = job_element.find_element(By.CSS_SELECTOR, job_title_selector).text
        job_url_element = job_element.find_element(By.CSS_SELECTOR, job_url_selector)
        job_url = job_url_element.get_attribute("href") if job_url_element.get_attribute("href") else "#"
        job_listings.append({"Job-title": job_title, "URL": job_url})

    # Close the WebDriver
    driver.quit()

    # Print the JSON result
    print(json.dumps(job_listings, indent=4))

if __name__ == "__main__":
    main()
