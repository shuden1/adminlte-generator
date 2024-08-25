import json
import shutil
import sys
import threading
from selenium import webdriver
import os
from dotenv import load_dotenv

load_dotenv()
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service

# Step 1: Identify the exact HTML selectors
job_block_selector = ".w-vwrapper.align_none.valign_top"  # Blocks with Job Openings
job_title_selector = "h6"  # Job Titles
job_url_selector = ".career-details a"  # URLs

# Step 2: Create a Python + Selenium script
def scrape_job_listings(html_file_name):

    result = []

    profile_folder_path = os.getenv("CHROME_PROFILE_PATH") + os.path.sep + str(threading.get_ident())

    service = Service(executable_path=r""+os.getenv("CHROME_DRIVER_PATH")+"")
    options = webdriver.ChromeOptions()
    options.add_argument(f"user-data-dir={profile_folder_path}")
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")

    driver = webdriver.Chrome(service=service, options=options)
    driver.get(f"file:///{html_file_name}")

    job_blocks = driver.find_elements(By.CSS_SELECTOR, job_block_selector)

    for block in job_blocks:
        title_elements = block.find_elements(By.CSS_SELECTOR, job_title_selector)
        url_elements = block.find_elements(By.CSS_SELECTOR, job_url_selector)
        for title_element, url_element in zip(title_elements, url_elements):
            job_title = title_element.text.strip()
            job_url = url_element.get_attribute("href")
            result.append({"Job-title": job_title, "URL": job_url})

    driver.quit()


    return json.dumps(result)

if __name__ == "__main__":
    html_file_name = sys.argv[1]
    print(scrape_job_listings(html_file_name))
