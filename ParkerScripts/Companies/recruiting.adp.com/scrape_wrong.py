import sys
from selenium import webdriver
import os
from dotenv import load_dotenv

load_dotenv()
from selenium.webdriver.common.by import By
import threading
import shutil
import json

# Take the HTML file name from the command line argument
html_file_path = sys.argv[1]

# Selenium WebDriver setup
profile_folder_path = os.getenv("CHROME_PROFILE_PATH") + os.path.sep + str(threading.get_ident())
options = webdriver.ChromeOptions()
options.add_argument(f"user-data-dir={profile_folder_path}")
options.add_argument("--headless")
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")
service = webdriver.chrome.service.Service(executable_path=r""+os.getenv("CHROME_DRIVER_PATH")+"")
driver = webdriver.Chrome(service=service, options=options)

# Open local HTML file
driver.get(f"file://{html_file_path}")

# Scraping job listings
job_blocks = driver.find_elements(By.CSS_SELECTOR, "div.job-listing")
job_listings = []
for job_block in job_blocks:
    job_title_elements = job_block.find_elements(By.CSS_SELECTOR, "h2 > a[href]")
    for job_title_element in job_title_elements:
        job_title = job_title_element.text.strip()
        job_url = job_title_element.get_attribute('href')
        job_listings.append({"Job-title": job_title, "URL": job_url})

# Convert list to JSON
job_listings_json = json.dumps(job_listings)

# Output the result as JSON
print(job_listings_json)

# Clean up
driver.quit()
# shutil.rmtree(profile_folder_path, ignore_errors=True)
