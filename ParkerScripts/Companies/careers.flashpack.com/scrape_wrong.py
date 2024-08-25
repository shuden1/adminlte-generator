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
    profile_folder_path = os.getenv("CHROME_PROFILE_PATH") + "\\" + str(threading.get_ident())
    service = Service(executable_path=r""+os.getenv("CHROME_DRIVER_PATH")+"")

    options = Options()
    options.add_argument(f"user-data-dir={profile_folder_path}")
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")

    driver = webdriver.Chrome(service=service, options=options)

    driver.get(f"file:///{file_path}")

    job_blocks_selector = 'div[class*="job"], ul[class*="job"] > li'
    job_title_selector = 'a, h2 a, h3 a, p a'

    job_blocks = driver.find_elements(By.CSS_SELECTOR, job_blocks_selector)

    job_postings = []
    for block in job_blocks:
        title_tag = block.find_element(By.CSS_SELECTOR, job_title_selector)
        job_title = title_tag.text.strip()
        job_url = title_tag.get_attribute('href')
        job_postings.append({"Job-title": job_title, "URL": job_url})

    driver.quit()

    return json.dumps(job_postings, indent=4)

if __name__ == "__main__":
    file_path = sys.argv[1]
    print(scrape_jobs(file_path))
