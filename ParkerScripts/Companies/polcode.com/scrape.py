import sys
from selenium import webdriver
import os
from dotenv import load_dotenv

load_dotenv()
from selenium.webdriver.chrome.service import Service as ChromeService
import threading
from selenium.webdriver.common.by import By
import json

# Retrieving the target HTML file name from console command
target_html_file = sys.argv[1]

# Setting up Chrome options
options = webdriver.ChromeOptions()
profile_folder_path = os.getenv("CHROME_PROFILE_PATH") + "\\" + str(threading.get_ident())
options.add_argument(f"user-data-dir={profile_folder_path}")
options.add_argument("--headless")
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")

# Setting up Chrome service
service = ChromeService(executable_path=r""+os.getenv("CHROME_DRIVER_PATH")+"")

# Initializing the Chrome driver
driver = webdriver.Chrome(service=service, options=options)

# Opening the target HTML file
driver.get(f"file:///{target_html_file}")

# Defining the selectors based on the analysis
job_opening_blocks_selector = ".grid.lg\\:grid-cols-3.grid-cols-1.sm\\:grid-cols-2.gap-8.pt-10"
job_link_selector = "a"
job_title_selector = "h3"

# Extracting job titles and URLs
job_blocks = driver.find_elements(By.CSS_SELECTOR, job_opening_blocks_selector)
jobs = []

for job_block in job_blocks:
    job_links = job_block.find_elements(By.CSS_SELECTOR, job_link_selector)
    for job_link in job_links:
        job_title = job_link.find_element(By.CSS_SELECTOR, job_title_selector).text
        job_url = job_link.get_attribute('href')
        jobs.append({"Job-title": job_title, "URL": job_url})

driver.quit()

# Printing the extracted jobs in JSON format
print(json.dumps(jobs))
