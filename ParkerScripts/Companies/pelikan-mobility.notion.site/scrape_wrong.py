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
    profile_folder_path = os.getenv("CHROME_PROFILE_PATH") + "\\" + str(threading.get_ident())
    service = Service(executable_path=r""+os.getenv("CHROME_DRIVER_PATH")+"")

    options = Options()
    options.add_argument(f"user-data-dir={profile_folder_path}")
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")

    driver = webdriver.Chrome(service=service, options=options)

    driver.get(f"file:///{file_path}")

    job_block_selector = 'div.notion-app-inner.notion-light-theme'
    job_title_selector = 'a'

    job_blocks = driver.find_elements(By.CSS_SELECTOR, job_block_selector)

    job_postings = []
    for block in job_blocks:
        titles = block.find_elements(By.CSS_SELECTOR, job_title_selector)
        for title in titles:
            job_title = title.get_attribute('innerText').strip()
            job_url = title.get_attribute('href')
            if job_title and job_url:
                job_postings.append({
                    "Job-title": job_title,
                    "URL": job_url
                })

    driver.quit()

    print(json.dumps(job_postings, indent=4))

if __name__ == "__main__":
    file_path = sys.argv[1]
    scrape_jobs(file_path)
