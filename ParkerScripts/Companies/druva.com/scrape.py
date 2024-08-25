import sys
import threading
import shutil
import json
from selenium import webdriver
import os
from dotenv import load_dotenv

load_dotenv()
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By

# The target HTML file name should be an argument sent from an external source through the console command
html_file_name = sys.argv[1]

# Initialize a headless webdriver
profile_folder_path = f"{os.getenv("CHROME_PROFILE_PATH")}{os.path.sep}{threading.get_ident()}"
service = Service(executable_path=r""+os.getenv("CHROME_DRIVER_PATH")+"")
options = webdriver.ChromeOptions()
options.add_argument(f"user-data-dir={profile_folder_path}")
options.add_argument("--headless")
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")

driver = webdriver.Chrome(service=service, options=options)

try:
    # Open the local HTML file
    driver.get(f"file:///{html_file_name}")

    # Selectors based on the BeautifulSoup analysis
    job_block_selector = ".druvaJobs-department"
    job_title_selector = ".druvaJobs-jobTitle"

    job_listings = []

    # FIND THE ELEMENTS USING THE PROVIDED SELECTORS
    for job_block in driver.find_elements(By.CSS_SELECTOR, job_block_selector):
        for job_title in job_block.find_elements(By.CSS_SELECTOR, job_title_selector):
            title = job_title.text.strip()
            url = job_title.get_attribute('href').strip()
            job_listings.append({"Job-title": title, "URL": url})

    # Return a JSON
    print(json.dumps(job_listings))

finally:
    # Clean up
    driver.quit()
