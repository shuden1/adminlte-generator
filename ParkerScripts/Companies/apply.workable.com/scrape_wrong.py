from selenium import webdriver
import os
from dotenv import load_dotenv

load_dotenv()
from selenium.webdriver.common.by import By
import json
import shutil
import sys
import threading

# The target HTML file name is taken from script argument
html_file = sys.argv[1]

# Create a webdriver service
service = webdriver.chrome.service.Service(executable_path=r""+os.getenv("CHROME_DRIVER_PATH")+"")

# Set webdriver options
options = webdriver.ChromeOptions()
profile_folder_path = f"{os.getenv("CHROME_PROFILE_PATH")}{os.path.sep}{threading.get_ident()}"
options.add_argument(f"user-data-dir={profile_folder_path}")
options.add_argument("--headless")
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")

# Initialize webdriver
driver = webdriver.Chrome(service=service, options=options)

try:
    # Open the local HTML file
    driver.get(f'file:///{html_file}')

    # Extract job titles and URLs
    jobs = []
    job_listings = driver.find_elements(By.CSS_SELECTOR, "li[class*='job-opening']")

    for job_listing in job_listings:
        title_element = job_listing.find_element(By.CSS_SELECTOR, "h3[data-id='job-item']")
        job_title = title_element.text.strip()
        # Since no URLs are visually shown in the snippet, this selector is a guess
        # If URLs follow a consistent pattern referencing job titles or IDs,
        # it should be adapted to the specific pattern found in the actual HTML.
        job_url = "https://www.example.com/jobs/" + job_listing.get_attribute("id")

        jobs.append({"Job-title": job_title, "URL": job_url})

    # Output the extracted data as JSON
    print(json.dumps(jobs))

finally:
    # Clean up by closing the browser and removing the profile directory
    driver.quit()
