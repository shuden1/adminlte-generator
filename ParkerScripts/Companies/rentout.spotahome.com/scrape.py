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
    # Get the target HTML file name from the console command
    target_html_file = sys.argv[1]

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

    # Load the target HTML file
    driver.get(f"file:///{target_html_file}")

    # Define the selectors
    job_opening_selector = 'a.job-box-link.job-box'
    job_title_selector = 'div.jb-title'
    job_url_attribute = 'href'

    # Find all job openings
    job_elements = driver.find_elements(By.CSS_SELECTOR, job_opening_selector)

    # Extract job titles and URLs
    jobs = []
    for job_element in job_elements:
        title_element = job_element.find_element(By.CSS_SELECTOR, job_title_selector)
        job_title = title_element.text.strip()
        job_url = job_element.get_attribute(job_url_attribute)
        jobs.append({"Job-title": job_title, "URL": job_url})

    # Close the WebDriver
    driver.quit()

    # Return the result as JSON
    print(json.dumps(jobs, indent=4))

if __name__ == "__main__":
    main()
