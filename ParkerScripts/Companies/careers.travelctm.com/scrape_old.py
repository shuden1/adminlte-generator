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

    jobBlockSelector = "div[class*='job'], ul[class*='job'], div[class*='career'], ul[class*='career']"
    jobTitleSelector = "a[href*='jobs']:not([aria-label*='Apply']):not([aria-label*='Refer'])"

    job_blocks = driver.find_elements(By.CSS_SELECTOR, jobBlockSelector)

    job_postings = []
    for job_block in job_blocks:
        title_elements = job_block.find_elements(By.CSS_SELECTOR, jobTitleSelector)
        for title_element in title_elements:
            title_text = title_element.text.strip()
            if title_text:  # Ensure title is not empty
                job_postings.append({
                    "Job-title": title_text,
                    "URL": title_element.get_attribute("href")
                })

    driver.quit()

    print(json.dumps(job_postings, indent=4))

if __name__ == "__main__":
    file_path = sys.argv[1]
    scrape_jobs(file_path)
