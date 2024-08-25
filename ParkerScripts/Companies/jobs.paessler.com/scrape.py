import sys
from bs4 import BeautifulSoup
from selenium import webdriver
import os
from dotenv import load_dotenv

load_dotenv()
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import threading
import shutil
import json

# Argument is accepted through command line
html_file_path = sys.argv[1]

# Initialise a headless webdriver
profile_folder_path = os.getenv("CHROME_PROFILE_PATH") + os.path.sep + str(threading.get_ident())

service = Service(executable_path=r""+os.getenv("CHROME_DRIVER_PATH")+"")
options = Options()
options.add_argument(f"user-data-dir={profile_folder_path}")
options.add_argument("--headless")
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")

driver = webdriver.Chrome(service=service, options=options)

# Open the local HTML file
driver.get(f"file://{html_file_path}")

# Scrape all job listings
job_sections = driver.find_elements(By.CSS_SELECTOR, ".joboffer_container")
job_listings = []

for job_section in job_sections:
    title_element = job_section.find_element(By.CSS_SELECTOR, ".joboffer_title_text.joboffer_box a")
    job_title = title_element.text
    job_url = title_element.get_attribute('href')
    job_listings.append({"Job-title": job_title, "URL": job_url})

driver.quit()

# Remove the profile folder


# Output
print(json.dumps(job_listings))
