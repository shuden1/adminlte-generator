from selenium import webdriver
import os
from dotenv import load_dotenv

load_dotenv()
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
import json
import shutil
import sys
import threading

# Getting HTML file name from the argument
html_file_name = sys.argv[1]

# Initialise a headless webdriver
profile_folder_path = os.getenv("CHROME_PROFILE_PATH") + "\\" + str(threading.get_ident())
service = ChromeService(executable_path=r""+os.getenv("CHROME_DRIVER_PATH")+"")
options = webdriver.ChromeOptions()
options.add_argument(f"user-data-dir={profile_folder_path}")
options.add_argument("--headless")
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")

driver = webdriver.Chrome(service=service, options=options)

# Open the local HTML file
driver.get(f"file://{html_file_name}")

# Define the selectors from Step 1 (Based on the HTML file provided)
job_blocks_selector = "ul > div > li"
job_title_selector = ".css-7ebljt > a"
job_url_selector = ".css-7ebljt > a"

# Scrape all job listings
job_listings = []
job_blocks = driver.find_elements(By.CSS_SELECTOR, job_blocks_selector)
for job_block in job_blocks:
    job_title_element = job_block.find_element(By.CSS_SELECTOR, job_title_selector)
    title = job_title_element.text.strip()
    url = job_title_element.get_attribute('href')
    job_listings.append({"Job-title": title, "URL": url})

# Returning JSON format
print(json.dumps(job_listings))

# Close the driver and remove the profile folder
driver.quit()
