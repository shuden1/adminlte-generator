import sys
import json
import threading
import shutil
from selenium import webdriver
import os
from dotenv import load_dotenv

load_dotenv()
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By

# 1) Take the target HTML file name from an argument sent from an external source.
target_html_file = sys.argv[1]

# 2) Setup the headless webdriver.
profile_folder_path = os.getenv("CHROME_PROFILE_PATH") + os.path.sep + str(threading.get_ident())
service = ChromeService(executable_path=r""+os.getenv("CHROME_DRIVER_PATH")+"")
options = webdriver.ChromeOptions()
options.add_argument(f"user-data-dir={profile_folder_path}")
options.add_argument("--headless")
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")

# 3) Start the web driver and open the local HTML file.
driver = webdriver.Chrome(service=service, options=options)
driver.get(f"file:///{target_html_file}")

# 4) Scrape all job listings using the selectors from STEP 1.
job_listings = []
job_elements = driver.find_elements(By.CSS_SELECTOR, "a.job[data-color='default']")
for job_element in job_elements:
    title_element = job_element.find_element(By.CSS_SELECTOR, "div.title.fw-bold.m-b-8")
    job_title = title_element.text.strip()
    job_url = job_element.get_attribute("href")
    job_listings.append({"Job-title": job_title, "URL": job_url})

# 5) Return a JSON-formatted list of job listings.
print(json.dumps(job_listings))

# 6) Close the driver and remove the profile folder.
driver.quit()
