import sys
from selenium import webdriver
import os
from dotenv import load_dotenv

load_dotenv()
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
import threading
import json
import re

# Accepting target HTML file name from console command
target_html_file = sys.argv[1]

# Webdriver setup
profile_folder_path = os.getenv("CHROME_PROFILE_PATH") + "\\" + str(threading.get_ident())
service = Service(executable_path=r""+os.getenv("CHROME_DRIVER_PATH")+"")
options = webdriver.ChromeOptions()
options.add_argument(f"user-data-dir={profile_folder_path}")
options.add_argument("--headless")
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")

# Start headless browser session
driver = webdriver.Chrome(service=service, options=options)

# Open the target HTML file
driver.get(f"file:///{target_html_file}")

# Selectors identified in Step 1
job_block_selector = ".posts_result"
job_title_selector = "h2.vc_headline.has-fontsize-h6"
job_url_selector = ".vc-content-box"

# Scraping job listings
job_elements = driver.find_elements(By.CSS_SELECTOR, job_block_selector)
jobs = []

for job_element in job_elements:
    title_element = job_element.find_element(By.CSS_SELECTOR, job_title_selector)
    onclick_attribute = job_element.find_element(By.CSS_SELECTOR, job_url_selector).get_attribute('onclick')
    jobs.append({"Job-title": title_element.text, "URL": re.search(r'window.open\("([^"]*)', onclick_attribute).group(1)})

# Output result
print(json.dumps(jobs))

# Close browser session
driver.quit()
