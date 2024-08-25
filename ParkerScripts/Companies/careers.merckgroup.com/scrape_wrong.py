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

def scrape_jobs(html_file_path):
    profile_folder_path = os.getenv("CHROME_PROFILE_PATH") + "\\" + str(threading.get_ident())
    service = Service(executable_path=r""+os.getenv("CHROME_DRIVER_PATH")+"")

    options = Options()
    options.add_argument(f"user-data-dir={profile_folder_path}")
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")

    driver = webdriver.Chrome(service=service, options=options)

    try:
        driver.get(f"file:///{html_file_path}")

        job_blocks = driver.find_elements(By.CSS_SELECTOR, '.smart-highlights.job-info')
        job_postings = []

        for block in job_blocks:
            links = block.find_elements(By.CSS_SELECTOR, 'a')
            for link in links:
                job_title = link.text.strip()
                job_url = link.get_attribute('href')
                if job_title and job_url:
                    job_postings.append({"Job-title": job_title, "URL": job_url})

        print(json.dumps(job_postings, indent=4))

    finally:
        driver.quit()

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script.py <html_file_path>")
        sys.exit(1)

    html_file_path = sys.argv[1]
    scrape_jobs(html_file_path)
