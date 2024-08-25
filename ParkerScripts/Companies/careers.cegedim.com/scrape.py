import sys
from selenium import webdriver
import os
from dotenv import load_dotenv

load_dotenv()
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
import threading
import json

# The target HTML file name is provided as a command-line argument
html_file_name = sys.argv[1]

# Set up Chrome options for headless execution
options = webdriver.ChromeOptions()
profile_folder_path = os.getenv("CHROME_PROFILE_PATH") + os.path.sep + str(threading.get_ident())
options.add_argument(f"user-data-dir={profile_folder_path}")
options.add_argument("--headless")
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")

# Set up the service
service = ChromeService(executable_path=r""+os.getenv("CHROME_DRIVER_PATH")+"")

# Initialize the driver with the specified service and options
driver = webdriver.Chrome(service=service, options=options)

# Load the web page from the local HTML file
driver.get(f"file:///{html_file_name}")

# Scrape job listings using the defined selectors
job_listings = []
elements = driver.find_elements(By.CSS_SELECTOR, ".job-ad-card__link.job-ad-card__link--square")
for element in elements:
    title_element = element.find_element(By.CSS_SELECTOR, ".job-ad-card__description-title")
    job_title = title_element.text
    job_url = element.get_attribute('href')
    job_listings.append({"Job-title": job_title, "URL": job_url})

# Close the driver
driver.quit()

# Convert the list of job listings to JSON and print it
print(json.dumps(job_listings))
