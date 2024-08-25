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

# Receive the HTML file name from the command line argument
html_file_name = sys.argv[1]

# Initialize the headless webdriver with the given profile path
profile_folder_path = os.getenv("CHROME_PROFILE_PATH") + "\\" + str(threading.get_ident())
service = ChromeService(executable_path=r""+os.getenv("CHROME_DRIVER_PATH")+"")
options = webdriver.ChromeOptions()
options.add_argument(f"user-data-dir={profile_folder_path}")
options.add_argument("--headless")
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")

driver = webdriver.Chrome(service=service, options=options)

# Open the local HTML file
driver.get(f"file:///{html_file_name}")

# Get the list of job postings using the selectors identified in Step 1
job_blocks_selector = ".gnewtonCareerGroupRowClass"
job_title_selector = ".gnewtonCareerGroupJobTitleClass a"

job_elements = driver.find_elements(By.CSS_SELECTOR, job_blocks_selector)

# Extract the titles and URLs
jobs = [
    {"Job-title": element.find_element(By.CSS_SELECTOR, job_title_selector).text, "URL": element.find_element(By.CSS_SELECTOR, job_title_selector).get_attribute('href')}
    for element in job_elements
]

# Output in the required JSON format
print(json.dumps(jobs))

# Close the driver and remove the profile folder
driver.quit()
