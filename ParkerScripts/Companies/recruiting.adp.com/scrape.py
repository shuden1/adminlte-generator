from selenium import webdriver
import os
from dotenv import load_dotenv

load_dotenv()
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
import sys
import shutil
import threading
import json

# Read the target HTML file name from the console command
html_file = sys.argv[1]

# Define the profile path for the headless webdriver based on thread identity
profile_folder_path = os.getenv("CHROME_PROFILE_PATH") + "\\" + str(threading.get_ident())

# Initialise a headless webdriver
service = ChromeService(executable_path=r""+os.getenv("CHROME_DRIVER_PATH")+"")
options = webdriver.ChromeOptions()
options.add_argument(f"user-data-dir={profile_folder_path}")
options.add_argument("--headless")
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")
driver = webdriver.Chrome(service=service, options=options)

# Open the HTML file
driver.get(f"file:///{html_file}")

# Job opening blocks and their title and URL selectors
job_blocks_selector = '.col-sm-12.nopadding.resultrow'
job_title_selector = 'a.job-title-link'
job_url_attribute = 'href'

# Scrape all job listings
job_listings = []
job_elements = driver.find_elements(By.CSS_SELECTOR, job_blocks_selector)
for job_elem in job_elements:
    job_title = job_elem.find_element(By.CSS_SELECTOR, job_title_selector).text
    job_url = "https://recruiting.adp.com/srccar/public/RTI.home?c=2190231&d=ExternalCBTS"
    job_listings.append({"Job-title": job_title, "URL": job_url})

# Output the job listings as JSON
print(json.dumps(job_listings))

# Close the driver and remove the profile folder
driver.quit()

