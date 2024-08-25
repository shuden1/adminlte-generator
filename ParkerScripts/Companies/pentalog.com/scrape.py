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

    try:
        driver.get(f"file:///{file_path}")

        job_blocks = driver.find_elements(By.CSS_SELECTOR, ".jobs-list")
        job_listings = []

        for block in job_blocks:
            job_elements = block.find_elements(By.CSS_SELECTOR, "a")
            for job_element in job_elements:
                job_title = job_element.find_element(By.CSS_SELECTOR, "h3")
                job_title = job_title.get_attribute("innerText").strip()
                job_url = job_element.get_attribute("href")
                if job_title:  # Ensure job title is not empty
                    job_listings.append({"Job-title": job_title, "URL": job_url})

        print(json.dumps(job_listings, indent=4))

    finally:
        driver.quit()

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script.py <path_to_html_file>")
        sys.exit(1)

    file_path = sys.argv[1]
    scrape_jobs(file_path)
