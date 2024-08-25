from selenium import webdriver
import os
from dotenv import load_dotenv

load_dotenv()
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
import json
import sys
import threading

# Extract the target HTML filename from the command line argument
target_html_file = sys.argv[1]

# Set up ChromeDriver with specified options
options = webdriver.ChromeOptions()
profile_folder_path = os.getenv("CHROME_PROFILE_PATH") + "\\" + str(threading.get_ident())
options.add_argument(f"user-data-dir={profile_folder_path}")
options.add_argument("--headless")
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")
service = ChromeService(executable_path=r""+os.getenv("CHROME_DRIVER_PATH")+"")

# Initialize driver with options
driver = webdriver.Chrome(service=service, options=options)

# Open the target HTML file with the driver
driver.get(f"file:///{target_html_file}")

# Use the selectors defined in STEP 1: Class names for the job blocks, job titles and URLs
job_listings_selector = ".vacancy-card"
job_title_selector = ".vacancy-card__title"
job_url_selector = ".vacancy-card__left"

# Initialize an empty list to hold the job listing information
job_listings = []

# Scrape all job listings using the selectors
job_elements = driver.find_elements(By.CSS_SELECTOR, job_listings_selector)
for job_element in job_elements:
    # Extract the job title and URL from each listing
    job_title_element = job_element.find_element(By.CSS_SELECTOR, job_title_selector)
    job_title = job_title_element.text.strip()

    job_url_element = job_element.find_element(By.CSS_SELECTOR, job_url_selector)
    job_url = job_url_element.get_attribute('href')

    # Append the job information as a dictionary to the job_listings list
    job_listings.append({"Job-title": job_title, "URL": job_url})

# Convert the job listings to JSON format
job_listings_json = json.dumps(job_listings)

# Print the JSON string
print(job_listings_json)

# Quit the Selenium WebDriver session
driver.quit()
