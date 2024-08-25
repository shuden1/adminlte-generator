import sys
import json
import shutil
import threading
from selenium import webdriver
import os
from dotenv import load_dotenv

load_dotenv()
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service

# Fetch the argument for the file name
html_file = sys.argv[1]

# Profile folder setup
profile_folder_path = (
    os.getenv("CHROME_PROFILE_PATH") + "\\"
    + str(threading.get_ident())
)
# shutil.rmtree(profile_folder_path, ignore_errors=True)

# Webdriver setup
service = Service(executable_path=r""+os.getenv("CHROME_DRIVER_PATH")+"")
options = webdriver.ChromeOptions()
options.add_argument(f"user-data-dir={profile_folder_path}")
options.add_argument("--headless")
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")

# Initialize webdriver
driver = webdriver.Chrome(service=service, options=options)
driver.implicitly_wait(10)

# Open the specified HTML file
driver.get(f"file:///{html_file}")

# Selector for job opening blocks
job_opening_block_selector = ".opportunity[data-bind*='Opportunity']"

# Selectors for job titles and URLs
job_title_selector = ".opportunity-link.break-word[data-automation='job-title']"

# Scraping job titles and URLs
job_data = []

try:
    job_blocks = driver.find_elements(By.CSS_SELECTOR, job_opening_block_selector)

    for block in job_blocks:
        job_link_element = block.find_element(By.CSS_SELECTOR, job_title_selector)
        job_title = job_link_element.text
        job_url = job_link_element.get_attribute('href')

        job_data.append({"Job-title": job_title, "URL": job_url})
except Exception as e:
    print(f"Error occurred: {e}")

finally:
    driver.quit()
    # shutil.rmtree(profile_folder_path, ignore_errors=True)

# Output the job data as JSON
print(json.dumps(job_data))
