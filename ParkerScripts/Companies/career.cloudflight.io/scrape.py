import sys
from selenium import webdriver
import os
from dotenv import load_dotenv

load_dotenv()
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
import threading
import json

# Argument from external source
target_html_file = sys.argv[1]

# Initialising a headless webdriver
profile_folder_path = os.getenv("CHROME_PROFILE_PATH") + os.path.sep + str(threading.get_ident())
service = ChromeService(executable_path=r""+os.getenv("CHROME_DRIVER_PATH")+"")
options = webdriver.ChromeOptions()
options.add_argument(f"user-data-dir={profile_folder_path}")
options.add_argument("--headless")
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")
driver = webdriver.Chrome(service=service, options=options)

try:
    # Loading the HTML file
    driver.get(f"file:///{target_html_file}")

    # Scraping job listings using the fixed selectors identified
    job_listings = []
    for job in driver.find_elements(By.CSS_SELECTOR, ".jobs-container .bg-block-background"):
        title_element = job.find_element(By.CSS_SELECTOR, "a")
        job_title = title_element.text
        job_url = title_element.get_attribute("href")
        job_listings.append({"Job-title": job_title, "URL": job_url})

    # Converting and printing the result as JSON
    print(json.dumps(job_listings, indent=4))
finally:
    driver.quit()
