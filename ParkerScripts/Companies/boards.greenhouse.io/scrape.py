from selenium import webdriver
import os
from dotenv import load_dotenv

load_dotenv()
from selenium.webdriver.common.by import By
import json
import shutil
import os
import sys
import threading

# Retrieve HTML file path from arguments
html_file_path = sys.argv[1]

# Set up Chrome Driver options and service
profile_folder_path = os.getenv("CHROME_PROFILE_PATH") + "\\" + str(threading.get_ident())
options = webdriver.ChromeOptions()
options.add_argument(f"user-data-dir={profile_folder_path}")
options.add_argument("--headless")
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")
service = webdriver.chrome.service.Service(executable_path=r""+os.getenv("CHROME_DRIVER_PATH")+"")

# Initialize driver with options and service
driver = webdriver.Chrome(options=options, service=service)

# Open the local HTML file
driver.get(f"file:///{html_file_path}")

# Selectors identified from BeautifulSoup in step 1
job_opening_selectors = ".opening"
job_title_and_url_selectors = "a[data-mapped='true']"

# Find all job openings using the identified selectors
job_openings = driver.find_elements(By.CSS_SELECTOR, job_opening_selectors)

# Scraping job titles and their associated URLs
job_listings = []
for job in job_openings:
    title_element = job.find_element(By.CSS_SELECTOR, job_title_and_url_selectors)
    job_title = title_element.text
    job_url = title_element.get_attribute("href")
    job_listings.append({"Job-title": job_title, "URL": job_url})

# Return the job listings in JSON format
print(json.dumps(job_listings))

# Clean up: Close driver and remove profile folder
driver.quit()
