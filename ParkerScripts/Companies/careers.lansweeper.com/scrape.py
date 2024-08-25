from selenium import webdriver
import os
from dotenv import load_dotenv

load_dotenv()
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import json
import shutil
import threading
import sys

# STEP 1: Identifying the Job Opening Blocks and their sub-selectors for STEP 2
# After analysing the HTML file, these are the most likely selectors based on the provided information
job_block_selector = ".sc-uzptka-1.brursv"
job_title_selector = ".sc-6exb5d-3.gnPPfQ .sc-6exb5d-1.doUFBm"

# STEP 2: Create a Python + Selenium script
# Argument passed from the external source through the console command as the single input parameter
target_html_file_name = sys.argv[1]

# Initialise a headless webdriver
profile_folder_path = os.getenv("CHROME_PROFILE_PATH") + "\\" + str(threading.get_ident())
service = Service(executable_path=r""+os.getenv("CHROME_DRIVER_PATH")+"")
options = webdriver.ChromeOptions()
options.add_argument(f"user-data-dir={profile_folder_path}")
options.add_argument("--headless")
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")

# Launch the webdriver
driver = webdriver.Chrome(service=service, options=options)

# Open the HTML file
driver.get(f"file:///{target_html_file_name}")

# Scrape all job listings
job_listings = []
job_blocks = driver.find_elements(By.CSS_SELECTOR, job_block_selector)
for block in job_blocks:
    job_links = block.find_elements(By.CSS_SELECTOR, job_title_selector)
    for link in job_links:
        title = link.text
        url = link.get_attribute("href")
        job_listings.append({"Job-title": title, "URL": url})

# Print the JSON result
print(json.dumps(job_listings))

# End the session and remove the profile folder
driver.quit()
