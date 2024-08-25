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
    profile_folder_path = f"{os.getenv("CHROME_PROFILE_PATH")}{os.path.sep}{str(threading.get_ident())}"

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

    try:
        # Load the HTML file
        driver.get(f"file:///{html_file}")

        # Define the selectors
        job_opening_selector = "div.sc-beqWaB.sc-gueYoa.iUlpOy.MYFxR"
        job_title_selector = "div.sc-beqWaB.kToBwF[color='text.dark'][font-size='2,3'][font-weight='medium'][itemprop='title']"

        # Find all job openings
        job_openings = driver.find_elements(By.CSS_SELECTOR, job_opening_selector)

        job_listings = []

        for job in job_openings:
            try:
                # Extract job title
                job_title_element = job.find_element(By.CSS_SELECTOR, job_title_selector)
                job_title = job_title_element.text.strip() or job_title_element.get_attribute('innerHTML').strip()

                # Extract job URL
                try:
                    job_url_element = job.find_element(By.CSS_SELECTOR, "a")
                    job_url = job_url_element.get_attribute('href')
                except NoSuchElementException:
                    job_url = "#"

                job_listings.append({"Job-title": job_title, "URL": job_url})

            except NoSuchElementException:
                continue

        # Return the job listings as JSON
        print(json.dumps(job_listings, indent=4))

    finally:
        driver.quit()

if __name__ == "__main__":
    main()
