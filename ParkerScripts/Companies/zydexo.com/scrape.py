import sys
from selenium import webdriver
import os
from dotenv import load_dotenv

load_dotenv()
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
import threading
import json

# Assuming incorrect selectors from the initial script and not launching it
# Correcting the script to create a new, working script without syntax errors

# Target HTML file name received from the command line argument
html_file = sys.argv[1]

# Setting up Chrome WebDriver
options = webdriver.ChromeOptions()
profile_folder_path = os.getenv("CHROME_PROFILE_PATH") + os.path.sep+str(threading.get_ident())
service = ChromeService(executable_path=r""+os.getenv("CHROME_DRIVER_PATH")+"")

options.add_argument(f"user-data-dir={profile_folder_path}")
options.add_argument("--headless")
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")

# Initializing WebDriver
driver = webdriver.Chrome(service=service, options=options)

# Open the local HTML file
driver.get(f"file:///{html_file}")

# Scrape job titles and URLs using corrected selectors
jobs = []
job_blocks = driver.find_elements(By.CSS_SELECTOR, ".available_job_one")
for job_block in job_blocks:
    title_element = job_block.find_element(By.CSS_SELECTOR, ".job_title_heading > h3")
    url_element = job_block.find_element(By.CSS_SELECTOR, ".view_job_button > a")
    jobs.append({"Job-title": title_element.text, "URL": url_element.get_attribute('href')})

# Close the WebDriver
driver.quit()

# Return scraped jobs as JSON
print(json.dumps(jobs))
