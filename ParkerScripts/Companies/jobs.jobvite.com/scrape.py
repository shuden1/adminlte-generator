from bs4 import BeautifulSoup
import selenium.webdriver as webdriver
from selenium.webdriver.chrome.service import Service
import threading
import shutil
import json
import sys

# Selector definitions from step 1
block_selector = ".jv-job-list"
title_selector = ".jv-job-list-name a"
url_selector = ".jv-job-list-name a"

# Start of step 2 code

html_file = sys.argv[1]

# Create the profile folder
profile_folder_path = os.getenv("CHROME_PROFILE_PATH") + "\\" + str(threading.get_ident())
service = Service(executable_path=r""+os.getenv("CHROME_DRIVER_PATH")+"")

# Initialise webdriver options
options = webdriver.ChromeOptions()
options.add_argument(f"user-data-dir={profile_folder_path}")
options.add_argument("--headless")
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")

# Start driver
driver = webdriver.Chrome(service=service, options=options)

# Open the HTML file
driver.get(f"file:///{html_file}")

# Scrape job listings
job_list = []
job_elements = driver.find_elements(by=webdriver.common.by.By.CSS_SELECTOR, value=block_selector)
for job_element in job_elements:
    title_elements = job_element.find_elements(by=webdriver.common.by.By.CSS_SELECTOR, value=title_selector)
    for title_element in title_elements:
        job_title = title_element.text
        job_url = title_element.get_attribute('href')
        job_list.append({"Job-title": job_title, "URL": job_url})

# Convert the job listings to JSON format
job_list_json = json.dumps(job_list, indent=4)

print(job_list_json)

# Clean up the profile folder
driver.quit()
