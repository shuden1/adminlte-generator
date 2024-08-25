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
    html_file_path = sys.argv[1]

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

    try:
        # Load the HTML file
        driver.get(f"file:///{html_file_path}")

        # Define the selectors
        job_opening_selector = "a.jss-f72[href]"
        job_title_selector = "a.jss-f72[href]"
        job_url_selector = "a.jss-f72[href]"

        # Find all job opening elements
        job_opening_elements = driver.find_elements(By.CSS_SELECTOR, job_opening_selector)

        # Extract job titles and URLs
        job_listings = []
        for element in job_opening_elements:
            job_title = element.get_attribute('innerHTML').strip()
            job_url = element.get_attribute('href') or "#"
            job_listings.append({"Job-title": job_title, "URL": job_url})

        # Print the result as JSON
        print(json.dumps(job_listings, indent=4))

    finally:
        # Quit the WebDriver
        driver.quit()

if __name__ == "__main__":
    main()
