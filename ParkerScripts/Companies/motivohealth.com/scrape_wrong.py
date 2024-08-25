import sys
import threading
from selenium import webdriver
import os
from dotenv import load_dotenv

load_dotenv()
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By

# The target HTML file name comes from an external source (first argument passed to the script)
html_file_path = sys.argv[1]

# Initialize the headless WebDriver with the specified profile and options
profile_folder_path = os.getenv("CHROME_PROFILE_PATH") + os.path.sep + str(threading.get_ident())
service = ChromeService(executable_path=r""+os.getenv("CHROME_DRIVER_PATH")+"")
options = webdriver.ChromeOptions()
options.add_argument(f"user-data-dir={profile_folder_path}")
options.add_argument("--headless")
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")

driver = webdriver.Chrome(service=service, options=options)

try:
    # Load the HTML file
    driver.get(f"file:///{html_file_path}")

    # Define the selector for job listings from the refinement process
    job_listings_selector = '.MuiBox-root'

    # Use the selector to find all job elements
    job_elements = driver.find_elements(By.CSS_SELECTOR, job_listings_selector)

    # Extract job titles and URLs
    job_listings = []
    for job_element in job_elements:
        job_title_elements = job_element.find_elements(By.CSS_SELECTOR, 'a')  # Fixed typo in variable name
        for job_title_element in job_title_elements:  # Fixed incorrectly named loop variable
            job_title = job_title_element.text.strip()
            job_url = job_title_element.get_attribute('href')
            if '/careers' in job_url or 'job' in job_url:  # Filtering to ensure relevance to job listings
                job_listings.append({"Job-title": job_title, "URL": job_url})

    print(job_listings)

finally:
    driver.quit()
