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
    html_file_path = sys.argv[1]

    # Set up the Chrome driver with headless options
    profile_folder_path = f"{os.getenv("CHROME_PROFILE_PATH")}{os.path.sep}{str(threading.get_ident())}"
    service = Service(executable_path=r""+os.getenv("CHROME_DRIVER_PATH")+"")
    options = webdriver.ChromeOptions()
    options.add_argument(f"user-data-dir={profile_folder_path}")
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")

    driver = webdriver.Chrome(service=service, options=options)

    try:
        # Load the HTML file
        driver.get(f"file:///{html_file_path}")

        # Find all job postings
        job_postings = driver.find_elements(By.CSS_SELECTOR, 'a')

        jobs = []
        for job in job_postings:
            try:
                job_title = job.text.strip()
                if not job_title:
                    job_title = job.get_attribute('innerHTML').strip()

                job_url = job.get_attribute('href')
                if not job_url:
                    job_url = "#"

                jobs.append({"Job-title": job_title, "URL": job_url})
            except NoSuchElementException:
                continue

        # Return the job postings as JSON
        print(json.dumps(jobs, indent=4))

    finally:
        driver.quit()

if __name__ == "__main__":
    main()
