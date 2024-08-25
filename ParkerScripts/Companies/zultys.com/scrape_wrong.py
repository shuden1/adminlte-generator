import sys
import json
import shutil
import threading
from selenium import webdriver
import os
from dotenv import load_dotenv

load_dotenv()
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By

html_file_path = sys.argv[1]

profile_folder_path = os.getenv("CHROME_PROFILE_PATH") + os.path.sep+str(threading.get_ident())
service = Service(executable_path=r""+os.getenv("CHROME_DRIVER_PATH")+"")
options = webdriver.ChromeOptions()
options.add_argument(f"user-data-dir={profile_folder_path}")
options.add_argument("--headless")
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")

driver = webdriver.Chrome(service=service, options=options)
driver.get(f"file:///{html_file_path}")

job_listings = []

# Use the placeholder selectors replaced with actual selectors if available.
job_elements = driver.find_elements(By.CSS_SELECTOR, ".job-listing, .opening, .position")
for job_element in job_elements:
    title_elements = job_element.find_elements(By.CSS_SELECTOR, "h2.title, h3.title, a.title, span.title")
    for title_element in title_elements:
        job_listings.append({
            "Job-title": title_element.text,
            "URL": title_element.get_attribute('href')
        })

driver.quit()


print(json.dumps(job_listings))
