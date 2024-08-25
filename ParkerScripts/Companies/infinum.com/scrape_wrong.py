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
from selenium.webdriver.chrome.options import Options

def main():
    # Get the HTML file name from the command line argument
    html_file = sys.argv[1]

    # Set up the Chrome profile path
    profile_folder_path = os.getenv("CHROME_PROFILE_PATH") + os.path.sep + str(threading.get_ident())

    # Set up Chrome options
    options = Options()
    options.add_argument(f"user-data-dir={profile_folder_path}")
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")

    # Set up the Chrome service
    service = Service(executable_path=r""+os.getenv("CHROME_DRIVER_PATH")+"")

    # Initialize the WebDriver
    driver = webdriver.Chrome(service=service, options=options)

    try:
        # Load the HTML file
        driver.get(f"file:///{html_file}")

        # Find job postings
        job_postings = driver.find_elements(By.CSS_SELECTOR, "h2.card-simple__heading.typography.js-typography[data-id][class]")

        jobs = []

        for job in job_postings:
            try:
                job_title = job.text.strip()
                if not job_title:
                    job_title = job.get_attribute('innerHTML').strip()

                job_url_element = job.find_element(By.CSS_SELECTOR, "a")
                job_url = job_url_element.get_attribute('href') if job_url_element else "#"

                jobs.append({"Job-title": job_title, "URL": job_url})
            except NoSuchElementException:
                continue

        # Print the result as JSON
        print(json.dumps(jobs, indent=4))

    finally:
        driver.quit()

if __name__ == "__main__":
    main()
