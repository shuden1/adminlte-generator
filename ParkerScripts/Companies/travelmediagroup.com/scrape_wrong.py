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

    # Set up the ChromeDriver service and options
    profile_folder_path = f"{os.getenv("CHROME_PROFILE_PATH")}{os.path.sep}{threading.get_ident()}"
    service = Service(executable_path=r""+os.getenv("CHROME_DRIVER_PATH")+"")
    options = Options()
    options.add_argument(f"user-data-dir={profile_folder_path}")
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")

    # Initialize the WebDriver
    driver = webdriver.Chrome(service=service, options=options)

    # Load the HTML file
    driver.get(f"file:///{html_file_path}")

    # Define the selectors
    job_block_selector = 'div.et_pb_text_inner'
    job_title_selector = 'a'
    job_url_selector = 'a'

    # Find all job blocks
    job_blocks = driver.find_elements(By.CSS_SELECTOR, job_block_selector)

    job_postings = []

    # Extract job titles and their associated URLs
    for block in job_blocks:
        title_elements = block.find_elements(By.CSS_SELECTOR, job_title_selector)
        for title_element in title_elements:
            job_title = title_element.text.strip()
            job_url = title_element.get_attribute('href')
            if job_title and job_url and 'apply' in job_title.lower():
                job_postings.append({"Job-title": job_title, "URL": job_url})

    # Close the WebDriver
    driver.quit()

    # Print the JSON result
    print(json.dumps(job_postings, indent=4))

if __name__ == "__main__":
    main()
