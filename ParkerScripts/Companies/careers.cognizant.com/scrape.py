import sys
import json
import threading
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException

def main():
    # Get the HTML file name from the command line argument
    html_file = sys.argv[1]

    # Set up the Chrome options
    profile_folder_path = f"D:\\Mind\\CRA\\AI_Experiments\\Job_Crawlers\\Peter\\adminlte-generator\\chrome_profile\\{threading.get_ident()}"
    options = Options()
    options.add_argument(f"user-data-dir={profile_folder_path}")
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")

    # Set up the Chrome service
    service = Service(executable_path=r"C:\Python3\chromedriver.exe")

    # Initialize the WebDriver
    driver = webdriver.Chrome(service=service, options=options)

    try:
        # Load the HTML file
        driver.get(f"file:///{html_file}")

        # Find all job opening elements
        job_openings = driver.find_elements(By.CSS_SELECTOR, "h2.card-title")

        job_listings = []

        for job_opening in job_openings:
            try:
                # Find the job title element
                job_title_element = job_opening.find_element(By.CSS_SELECTOR, "a.stretched-link.js-view-job")
                job_title = job_title_element.text.strip() or job_title_element.get_attribute('innerHTML').strip()

                # Find the job URL element
                job_url = job_title_element.get_attribute('href') or "#"

                job_listings.append({"Job-title": job_title, "URL": job_url})
            except NoSuchElementException:
                continue

        # Print the job listings as JSON
        print(json.dumps(job_listings, indent=4))

    finally:
        driver.quit()

if __name__ == "__main__":
    main()