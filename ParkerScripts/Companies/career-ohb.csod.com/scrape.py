import sys
from selenium import webdriver
import os
from dotenv import load_dotenv

load_dotenv()
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
import json
import threading

# Receive the HTML file name from the external source
file_name = sys.argv[1]

service = ChromeService(executable_path=r""+os.getenv("CHROME_DRIVER_PATH")+"")
profile_folder_path = os.getenv("CHROME_PROFILE_PATH") + os.path.sep + str(threading.get_ident())

options = webdriver.ChromeOptions()
options.add_argument(f"user-data-dir={profile_folder_path}")
options.add_argument("--headless")
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")

driver = webdriver.Chrome(service=service, options=options)
driver.get(f"file:///{file_name}")

jobs = []

for job in driver.find_elements(By.CSS_SELECTOR, ".p-panel.p-bg-white.p-p-md.p-bw-xs.p-bc-grey70.p-bs-solid.rounded-all"):
    title_element = job.find_element(By.CSS_SELECTOR, ".p-text.p-f-sz-md.p-t-primary50.p-f-w-6")
    link_element = job.find_element(By.CSS_SELECTOR, "a")
    job_title = title_element.text
    job_url = link_element.get_attribute('href')
    jobs.append({"Job-title": job_title, "URL": job_url})

print(json.dumps(jobs))
