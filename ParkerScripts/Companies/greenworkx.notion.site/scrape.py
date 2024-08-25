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

def main():
    # Get the target HTML file name from the command line argument
    target_html_file = sys.argv[1]

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
        # Load the target HTML file
        driver.get(f"file:///{target_html_file}")

        # Define the selectors
        job_opening_selector = 'div.notion-selectable.notion-page-block.notion-collection-item'
        job_title_selector = 'div[contenteditable="false"][data-content-editable-leaf="true"]'
        job_url_selector = 'a[href]'

        # Find all job listings
        job_elements = driver.find_elements(By.CSS_SELECTOR, job_opening_selector)

        # Extract job titles and URLs
        job_listings = []
        for job in job_elements:
            title_element = job.find_element(By.CSS_SELECTOR, job_title_selector)
            url_element = job.find_element(By.CSS_SELECTOR, job_url_selector)
            job_listings.append({
                "Job-title": title_element.text,
                "URL": url_element.get_attribute("href")
            })

        # Print the result as JSON
        print(json.dumps(job_listings, indent=4))

    finally:
        # Quit the WebDriver
        driver.quit()

if __name__ == "__main__":
    main()
