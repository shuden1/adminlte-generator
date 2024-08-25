import sys
from selenium import webdriver
import os
from dotenv import load_dotenv

load_dotenv()
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
import threading
import shutil
import json

# Receives the target HTML file name from an external source through the console command
html_file = sys.argv[1]

# Initializes a headless webdriver with a profile path
profile_folder_path = os.getenv("CHROME_PROFILE_PATH") + "\\" + str(threading.get_ident())
service = ChromeService(executable_path=r""+os.getenv("CHROME_DRIVER_PATH")+"")
options = webdriver.ChromeOptions()
options.add_argument(f"user-data-dir={profile_folder_path}")
options.add_argument("--headless")
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")

# Starts the webdriver
driver = webdriver.Chrome(service=service, options=options)

# Read the local HTML file
driver.get(f"file:///{html_file}")

# DEFINE SELECTORS from Step 1
job_blocks_selector = "ul li div.fabric-5qovnk-root.MuiBox-root.css-7ebljt"
job_titles_selector = "a"
job_urls_selector = "a"

# Scrape all job listings
jobs = []
elements = driver.find_elements(By.CSS_SELECTOR, job_blocks_selector)
for job_element in elements:
    title_element = job_element.find_element(By.CSS_SELECTOR, job_titles_selector)
    job_title = title_element.text
    job_url = title_element.get_attribute('href')
    jobs.append({"Job-title": job_title, "URL": job_url})

# Return a JSON formatted string of the jobs list
output = json.dumps(jobs)

print(output)

# Clean up by closing the driver and removing the profile folder
driver.quit()
