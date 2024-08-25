import json
import shutil
import sys
import threading
from selenium import webdriver
import os
from dotenv import load_dotenv

load_dotenv()
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.common.exceptions import InvalidArgumentException

# Retrieve the target HTML file name from the command line argument
target_html_file = sys.argv[1]

# Define the profile folder path for Chrome
profile_folder_path = os.getenv("CHROME_PROFILE_PATH") + os.path.sep + str(threading.get_ident())

# Set the options for the headless browser
options = webdriver.ChromeOptions()
options.add_argument(f"user-data-dir={profile_folder_path}")
options.headless = True

# Define the service for ChromeDriver
service = ChromeService(executable_path=r""+os.getenv("CHROME_DRIVER_PATH")+"")

# Start the headless browser
driver = webdriver.Chrome(service=service, options=options)

try:
    # Open the target HTML file in the browser
    driver.get(f"file:///{target_html_file}")

    # Selectors for job titles and URLs
    jobs_selector = "a[data-ph-at-id='header-links']:not([aria-label='header logo']):not([aria-label='Locations']):not([aria-label='Search Jobs'])"

    # Scrape all job listings
    jobs_elements = driver.find_elements(By.CSS_SELECTOR, jobs_selector)
    jobs_data = [{"Job-title": elem.get_attribute("aria-label"), "URL": elem.get_attribute("href")}
                 for elem in jobs_elements
                 if elem.get_attribute("href").startswith("https")]

    # Output the scraped job listings as JSON
    print(json.dumps(jobs_data))

finally:
    # Remove the profile folder path
    # shutil.rmtree(profile_folder_path, onerror=lambda function, path, excinfo: None)

    # Close the browser
    driver.quit()
