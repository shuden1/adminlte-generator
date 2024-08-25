import sys
import json
import threading
from selenium import webdriver
import os
from dotenv import load_dotenv

load_dotenv()
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

def scrape_jobs(file_path):
    profile_folder_path = os.getenv("CHROME_PROFILE_PATH") + os.path.sep + str(threading.get_ident())
    service = Service(executable_path=r""+os.getenv("CHROME_DRIVER_PATH")+"")

    options = Options()
    options.add_argument(f"user-data-dir={profile_folder_path}")
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")

    driver = webdriver.Chrome(service=service, options=options)

    driver.get(f"file:///{file_path}")

    job_data = []

    # Replace 'YOUR_JOB_BLOCK_SELECTOR' with the actual selector for job blocks
    job_blocks = driver.find_elements(By.CSS_SELECTOR, '.job-block-class')  # Update with correct class

    for block in job_blocks:
        # Replace 'YOUR_JOB_TITLE_SELECTOR' with the actual selector for job titles
        title_element = block.find_element(By.CSS_SELECTOR, '.job-title-class')  # Update with correct class
        title = title_element.text
        url = title_element.get_attribute('href')
        job_data.append({"Job-title": title, "URL": url})

    driver.quit()

    return json.dumps(job_data, indent=4)

if __name__ == "__main__":
    file_path = sys.argv[1]
    print(scrape_jobs(file_path))
