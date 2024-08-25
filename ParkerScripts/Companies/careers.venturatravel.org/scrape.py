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
    # Get the HTML file name from the command line argument
    html_file = sys.argv[1]

    # Define the profile folder path
    profile_folder_path = f"{os.getenv("CHROME_PROFILE_PATH")}{os.path.sep}{str(threading.get_ident())}"

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
    job_opening_selector = "div.joblist-item"
    job_title_selector = "h3.title"
    job_url_selector = "a[href]"

    # Find all job postings
    job_elements = driver.find_elements(By.CSS_SELECTOR, job_opening_selector)

    # Extract job details
    job_listings = []
    for job_element in job_elements:
        title_element = job_element.find_element(By.CSS_SELECTOR, job_title_selector)
        title = title_element.get_attribute('innerHTML').strip()

        url_elements = job_element.find_elements(By.CSS_SELECTOR, job_url_selector)
        url = url_elements[0].get_attribute('href') if url_elements else "#"

        job_listings.append({"Job-title": title, "URL": url})

    # Close the WebDriver
    driver.quit()

    # Print the job listings as JSON
    print(json.dumps(job_listings, indent=4))

if __name__ == "__main__":
    main()
