import sys
import json
import shutil
import threading
from selenium import webdriver
import os
from dotenv import load_dotenv

load_dotenv()
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By

html_file = sys.argv[1]

profile_folder_path = os.getenv("CHROME_PROFILE_PATH") + "\\" + str(threading.get_ident())
options = webdriver.ChromeOptions()
options.add_argument(f"user-data-dir={profile_folder_path}")
options.add_argument("--headless")
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")
service = ChromeService(executable_path=r""+os.getenv("CHROME_DRIVER_PATH")+"")
driver = webdriver.Chrome(service=service, options=options)

driver.get(f"file:///{html_file}")

job_blocks_selector = "ul[data-ph-at-id='jobs-list'] .jobs-list-item"
job_title_selector = "span[role='heading'] a"
job_url_selector = "span[role='heading'] a"

job_listings = driver.find_elements(By.CSS_SELECTOR, job_blocks_selector)
jobs_json = []

for job in job_listings:
    job_title = job.find_element(By.CSS_SELECTOR, job_title_selector).text.strip()
    job_url = job.find_element(By.CSS_SELECTOR, job_url_selector).get_attribute('href').strip()
    jobs_json.append({"Job-title": job_title, "URL": job_url})

print(json.dumps(jobs_json))

driver.quit()

