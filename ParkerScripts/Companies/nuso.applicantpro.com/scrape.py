from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
import threading
import shutil
import json
import sys


# The HTML file name is retrieved from the command line argument
html_file_name = sys.argv[1]


# STEP 1: BeautifulSoup code to determine correct selectors would go here
# This BeautifulSoup code has been manually executed to determine the selectors and job items structure.
# Exemplary identified selectors for job listings blocks and job titles with URLs are as follows:

# Block selector for job listings:
job_block_selector = ".job-result"

# Job title and URL selectors within the job listing block:
job_title_selector = ".job-name a"
job_url_selector = ".action-column a"


# Initialising a headless webdriver
profile_folder_path = "D:\\Mind\\CRA\\AI_Experiments\\Job_Crawlers\\Peter\\adminlte-generator\\chrome_profile\\" + str(threading.get_ident())

options = webdriver.ChromeOptions()
options.add_argument(f"user-data-dir={profile_folder_path}")
options.add_argument("--headless")
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")

service = ChromeService(executable_path=r"C:\Python3\chromedriver.exe")

driver = webdriver.Chrome(service=service, options=options)

try:
    driver.get(f"file://{html_file_name}")

    # Scrape all job listings using the defined selectors
    job_blocks = driver.find_elements(By.CSS_SELECTOR, job_block_selector)

    job_listings = []
    for job_block in job_blocks:
        title_element = job_block.find_element(By.CSS_SELECTOR, job_title_selector)
        url_element = job_block.find_element(By.CSS_SELECTOR, job_url_selector)

        job_listing = {
            "Job-title": title_element.text,
            "URL": url_element.get_attribute('href')
        }

        job_listings.append(job_listing)

    # Return the JSON result (no need to write to a file, just print it to stdout)
    print(json.dumps(job_listings))

finally:
    driver.quit()
