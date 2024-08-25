import sys
import json
import threading
from selenium import webdriver
import os
from dotenv import load_dotenv

load_dotenv()
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

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

    job_blocks = driver.find_elements(By.CSS_SELECTOR, 'li.block-grid-item')
    jobs = []

    for job in job_blocks:
        title_element = job.find_element(By.CSS_SELECTOR, 'span.company-link-style')
        url_element = job.find_element(By.CSS_SELECTOR, 'a')

        title = title_element.text.strip()
        url = url_element.get_attribute('href')

        jobs.append({"Job-title": title, "URL": url})

    driver.quit()

    return json.dumps(jobs, indent=4)

if __name__ == "__main__":
    file_path = sys.argv[1]
    print(scrape_jobs(file_path))
