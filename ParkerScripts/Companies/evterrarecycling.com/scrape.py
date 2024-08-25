from selenium import webdriver
import os
from dotenv import load_dotenv

load_dotenv()
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
import threading
import shutil
import sys
import json

# Arguments
html_file_name = sys.argv[1]

# Selectors
job_listing_selector = '.elementor-column.elementor-col-33.elementor-inner-column.elementor-element'
job_title_selector = 'h4.elementor-heading-title'
job_url_selector = 'a.elementor-button-link'

# Selenium config
profile_folder_path = os.getenv("CHROME_PROFILE_PATH") + os.path.sep + str(threading.get_ident())
service = ChromeService(executable_path=r""+os.getenv("CHROME_DRIVER_PATH")+"")
options = Options()
options.add_argument("--headless")
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")
options.add_argument(f"user-data-dir={profile_folder_path}")

# Webdriver Initialization
driver = webdriver.Chrome(service=service, options=options)
driver.get(f"file:///{html_file_name}")

# Scraping
job_openings = []
job_listings = driver.find_elements(By.CSS_SELECTOR, job_listing_selector)
for job_listing in job_listings:
    try:
        title_element = job_listing.find_element(By.CSS_SELECTOR, job_title_selector)
        url_element = job_listing.find_element(By.CSS_SELECTOR, job_url_selector)
        job_openings.append({"Job-title": title_element.text.strip(), "URL": url_element.get_attribute('href').strip()})
    except Exception as e:
        pass  # If any exception occurs (element not found), continue to the next job_listing element

driver.quit()

# Output
output_json = json.dumps(job_openings)
print(output_json)

# Cleanup
# shutil.rmtree(profile_folder_path, ignore_errors=True)
