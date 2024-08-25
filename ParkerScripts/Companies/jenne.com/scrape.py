import json
import shutil
import threading
from selenium import webdriver
import os
from dotenv import load_dotenv

load_dotenv()
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
import sys

# Step 1: Selectors identified using BeautifulSoup (Based on file analysis)
# Assuming the use of the provided HTML snippet to derive the selectors

job_block_selector = "div.gnewtonCareerGroupRowClass"
job_title_selector = "div.gnewtonCareerGroupJobTitleClass a"
job_url_selector = "div.gnewtonCareerGroupJobTitleClass a"

# Step 2: Create a Python + Selenium script

# The target HTML file name is received as an argument from the console command
html_file_path = sys.argv[1]

# Initializing a headless webdriver
profile_folder_path = os.getenv("CHROME_PROFILE_PATH") + os.path.sep + str(threading.get_ident())
service = ChromeService(executable_path=r""+os.getenv("CHROME_DRIVER_PATH")+"")
options = webdriver.ChromeOptions()
options.add_argument(f"user-data-dir={profile_folder_path}")
options.add_argument("--headless")
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")

driver = webdriver.Chrome(service=service, options=options)

jobs = []

try:
    # Open the local HTML file
    driver.get(f"file://{html_file_path}")

    # Scrape all job listings using the selectors defined in Step 1
    job_listings = driver.find_elements(By.CSS_SELECTOR, job_block_selector)
    for job_listing in job_listings:
        title_element = job_listing.find_element(By.CSS_SELECTOR, job_title_selector)
        job_title = title_element.text.strip()
        job_url = title_element.get_attribute('href').strip()
        jobs.append({"Job-title": job_title, "URL": job_url})

    # Return a JSON containing job titles and URLs
    print(json.dumps(jobs))

finally:
    driver.quit()
    # Remove the profile folder created earlier
    # shutil.rmtree(profile_folder_path, ignore_errors=True)
