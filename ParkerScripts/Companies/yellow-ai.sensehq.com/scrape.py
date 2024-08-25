# Required imports
import sys
import threading
import shutil
from selenium import webdriver
import os
from dotenv import load_dotenv

load_dotenv()
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
import json

# STEP 1: Parsing the HTML structure - BeautifulSoup has been used externally
# Job Openings block selector
job_openings_block_selector = ".css-1tk7xz5"
# Job Title and URL selectors within job openings block
job_title_selector = ".css-beqgbl > span"
job_url_selector = ".css-1eijxws"

# STEP 2: Python + Selenium script
def main(html_file_path):
    # The path to the user's profile directory
    profile_folder_path = f"D:\\Mind\\CRA\\AI_Experiments\\Job_Crawlers\\Peter\\adminlte-generator\\chrome_profile\\{threading.get_ident()}"

    # Creating the service
    service = Service(executable_path=r""+os.getenv("CHROME_DRIVER_PATH")+"")

    # Options for Chrome
    options = webdriver.ChromeOptions()
    options.add_argument(f"user-data-dir={profile_folder_path}")
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")

    # Initializing the WebDriver
    driver = webdriver.Chrome(service=service, options=options)

    # Open the HTML file
    driver.get(f"file:///{html_file_path}")

    # Scrape job listings data
    listings = driver.find_elements(By.CSS_SELECTOR, job_openings_block_selector)
    jobs = []

    for listing in listings:
        job_title = listing.find_element(By.CSS_SELECTOR, job_title_selector).text
        job_url = "https://yellow-ai.sensehq.com/careers"
        jobs.append({"Job-title": job_title, "URL": job_url})

    # Closing the browser
    driver.quit()

    # Removing the profile folder
    # shutil.rmtree(profile_folder_path, ignore_errors=True)

    # Return JSON format
    return json.dumps(jobs)

if __name__ == "__main__":
    # Getting the HTML file name from input parameter
    html_file_name = sys.argv[1]
    result = main(html_file_name)
    print(result)
