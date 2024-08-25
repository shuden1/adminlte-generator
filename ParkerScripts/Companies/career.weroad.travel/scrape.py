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

def scrape_jobs(file_path):
    # Profile folder path
    profile_folder_path = f"D:\\Mind\\CRA\\AI_Experiments\\Job_Crawlers\\Peter\\adminlte-generator\\chrome_profile\\{threading.get_ident()}"

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
        driver.get(f"file:///{file_path}")

        # Use the selectors defined in STEP 1 to find job listings
        job_elements = driver.find_elements(By.CSS_SELECTOR, 'a[href*="job"]')

        # Extract job titles and URLs
        jobs = []
        for job_element in job_elements:
            job_title = job_element.text.strip()
            job_url = job_element.get_attribute('href')
            jobs.append({"Job-title": job_title, "URL": job_url})

        # Return the job postings as JSON
        return json.dumps(jobs, indent=4)

    finally:
        # Quit the WebDriver
        driver.quit()

if __name__ == "__main__":
    # Get the file path from the command line argument
    file_path = sys.argv[1]
    # Scrape the jobs and print the result
    print(scrape_jobs(file_path))
