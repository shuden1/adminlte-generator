import json
import os
import shutil
import sys
import threading
from selenium import webdriver
import os
from dotenv import load_dotenv

load_dotenv()
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

# The script doesn't include explicit selectors since BeautifulSoup parsing was unproductive
# These selectors should replace 'job_block_selector' and 'job_title_selector'
job_block_selector = '.job-opening-block-selector'  # Placeholder class for job block
job_title_selector = '.job-opening-block-selector .job-title a'  # Placeholder class for job title and URL

# Get the target HTML file name sent from an external source through the console command as the single input parameter
html_file_path = sys.argv[1]

# Step 2 Script
def scrape_job_openings(target_html):
    profile_folder_path = os.getenv("CHROME_PROFILE_PATH") + "\\" + str(threading.get_ident())
    if not os.path.exists(profile_folder_path):
        os.makedirs(profile_folder_path)

    service = Service(executable_path=r""+os.getenv("CHROME_DRIVER_PATH")+"")
    options = Options()
    options.add_argument(f"user-data-dir={profile_folder_path}")
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")

    with webdriver.Chrome(service=service, options=options) as driver:
        driver.get(f"file://{target_html}")

        job_listings = []
        job_elements = driver.find_elements(By.CSS_SELECTOR, job_block_selector)

        for element in job_elements:
            jobs = element.find_elements(By.CSS_SELECTOR, job_title_selector)
            for job in jobs:
                title = job.text
                url = job.get_attribute('href')
                job_listings.append({"Job-title": title, "URL": url})


    return json.dumps(job_listings)

# Run the function and print out the results
print(scrape_job_openings(html_file_path))
