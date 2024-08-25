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
from selenium.common.exceptions import NoSuchElementException

def main():
    # Get the HTML file name from the command line argument
    html_file_path = sys.argv[1]

    # Define the profile folder path
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

    try:
        # Load the HTML file
        driver.get(f"file:///{html_file_path}")

        # Find job postings
        job_postings = driver.find_elements(By.CSS_SELECTOR, "div[class='sqs-html-content']")

        jobs = []
        for job in job_postings:
            try:
                title_element = job.find_element(By.CSS_SELECTOR, "h4[class='preFlex'][style='text-align: center; white-space: pre-wrap; transition-timing-function: cubic-bezier(0.19, 1, 0.22, 1); transition-duration: 0.65s;']")
                title = title_element.text.strip() if title_element.text.strip() else title_element.get_attribute('innerHTML').strip()
            except NoSuchElementException:
                title = "No Title"

            try:
                url_element = job.find_element(By.CSS_SELECTOR, "a")
                url = url_element.get_attribute('href').strip() if url_element.get_attribute('href').strip() else "#"
            except NoSuchElementException:
                url = "#"

            jobs.append({"Job-title": title, "URL": url})

        # Output the result as JSON
        print(json.dumps(jobs, indent=4))

    finally:
        driver.quit()

if __name__ == "__main__":
    main()
