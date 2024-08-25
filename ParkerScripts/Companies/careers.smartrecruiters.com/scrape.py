from selenium import webdriver
import os
from dotenv import load_dotenv

load_dotenv()
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import threading
import shutil
import sys
import json

target_html_file = sys.argv[1]

profile_folder_path = os.getenv("CHROME_PROFILE_PATH") + os.path.sep + str(threading.get_ident())
service = Service(executable_path=r""+os.getenv("CHROME_DRIVER_PATH")+"")
options = webdriver.ChromeOptions()
options.add_argument(f"user-data-dir={profile_folder_path}")
options.add_argument("--headless")
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")

driver = webdriver.Chrome(service=service, options=options)

driver.get(f"file:///{target_html_file}")

job_listings = []
opening_section_selector = '.openings-body'
job_title_and_url_selector = 'a.link--block.details'

openings = driver.find_elements(By.CSS_SELECTOR, opening_section_selector)
for opening in openings:
    jobs = opening.find_elements(By.CSS_SELECTOR, job_title_and_url_selector)
    for job in jobs:
        title = job.find_element(By.CSS_SELECTOR, 'h4.details-title.job-title').text.strip()
        url = job.get_attribute('href').strip()
        job_listings.append({"Job-title": title, "URL": url})

print(json.dumps(job_listings))

driver.quit()

