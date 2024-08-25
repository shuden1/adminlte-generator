import sys
from selenium import webdriver
import os
from dotenv import load_dotenv

load_dotenv()
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
import threading
import json

# The target HTML file name is taken from the command line argument
html_file = sys.argv[1]

# Webdriver setup
profile_folder_path = os.getenv("CHROME_PROFILE_PATH") + "\\" + str(threading.get_ident())
service = ChromeService(executable_path=r""+os.getenv("CHROME_DRIVER_PATH")+"")
options = webdriver.ChromeOptions()
options.add_argument(f"user-data-dir={profile_folder_path}")
options.add_argument("--headless")
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")

driver = webdriver.Chrome(service=service, options=options)

# Load the HTML file
driver.get(f"file:///{html_file}")

# Selectors defined in STEP 1
job_block_selector = ".vacancySection__item"
job_title_selector = ".vacancySection__info h3"
job_url_selector = ".vacancySection__info a"

# Extract job listings data
job_elements = driver.find_elements(By.CSS_SELECTOR, job_block_selector)
job_listings = []
for job_element in job_elements:
    title = job_element.find_element(By.CSS_SELECTOR, job_title_selector).text
    url = job_element.find_element(By.CSS_SELECTOR, job_url_selector).get_attribute('href')
    job_listings.append({"Job-title": title, "URL": url})

driver.quit()

# Format as JSON and print
print(json.dumps(job_listings))
