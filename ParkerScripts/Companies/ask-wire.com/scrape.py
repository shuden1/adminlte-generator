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
    profile_folder_path = f"{os.getenv("CHROME_PROFILE_PATH")}{os.path.sep}{str(threading.get_ident())}"
    service = Service(executable_path=r""+os.getenv("CHROME_DRIVER_PATH")+"")

    options = Options()
    options.add_argument(f"user-data-dir={profile_folder_path}")
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")

    driver = webdriver.Chrome(service=service, options=options)

    try:
        driver.get(f"file:///{file_path}")

        job_blocks = driver.find_elements(By.CSS_SELECTOR, 'a[aria-controls^="tab-strong"]')
        job_postings = []

        for block in job_blocks:
            title_element = block.find_element(By.CSS_SELECTOR, 'div.kb-tab-titles-wrap span.kt-title-text')
            if title_element.text.strip():  # Ensure the title is not empty
                job_postings.append({
                    "Job-title": title_element.text.strip(),
                    "URL": block.get_attribute('href')
                })

        print(json.dumps(job_postings, indent=4))

    finally:
        driver.quit()

if __name__ == "__main__":
    file_path = sys.argv[1]
    scrape_jobs(file_path)
