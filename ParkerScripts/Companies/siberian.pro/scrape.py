import sys
import json
import threading
from selenium import webdriver
import os
from dotenv import load_dotenv

load_dotenv()
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException

def main():
    # Get the HTML file name from the command line argument
    html_file = sys.argv[1]

    # Define the profile folder path
    profile_folder_path = os.getenv("CHROME_PROFILE_PATH") + "\\" + str(threading.get_ident())

    # Set up Chrome options
    options = webdriver.ChromeOptions()
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

    job_listings = []

    try:
        # Find all job opening elements
        job_elements = driver.find_elements(By.CSS_SELECTOR, "div.comment-author")

        for job_element in job_elements:
            try:
                # Extract job title
                title_element = job_element.find_element(By.CSS_SELECTOR, "span")
                job_title = title_element.text.strip() if title_element.text.strip() else title_element.get_attribute('innerHTML').strip()

                # Extract job URL (if exists)
                try:
                    url_element = job_element.find_element(By.CSS_SELECTOR, "a")
                    job_url = url_element.get_attribute('href').strip() if url_element.get_attribute('href').strip() else "#"
                except NoSuchElementException:
                    job_url = "#"

                job_listings.append({"Job-title": job_title, "URL": job_url})
            except NoSuchElementException:
                continue

    except NoSuchElementException:
        pass

    # Close the WebDriver
    driver.quit()

    # Print the job listings as JSON
    print(json.dumps(job_listings, ensure_ascii=False))

if __name__ == "__main__":
    main()
