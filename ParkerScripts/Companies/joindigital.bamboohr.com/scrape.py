import sys
from selenium import webdriver
import os
from dotenv import load_dotenv

load_dotenv()
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
import threading
import shutil
import json

def scrape_job_listings(html_file):
    profile_folder_path = f"{os.getenv("CHROME_PROFILE_PATH")}{os.path.sep}{str(threading.get_ident())}"
    service = ChromeService(executable_path=r""+os.getenv("CHROME_DRIVER_PATH")+"")
    options = webdriver.ChromeOptions()
    options.add_argument(f"user-data-dir={profile_folder_path}")
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")

    driver = webdriver.Chrome(service=service, options=options)

    try:
        driver.get(f"file:///{html_file}")

        jobs = []
        for job_element in driver.find_elements(By.CSS_SELECTOR, "ul > div > li"):
            title_element = job_element.find_element(By.CSS_SELECTOR, "a")
            job_title = title_element.text
            job_url = title_element.get_attribute("href")
            jobs.append({"Job-title": job_title, "URL": job_url})

        return json.dumps(jobs)
    finally:
        driver.quit()


if __name__ == "__main__":
    html_file_path = sys.argv[1]
    print(scrape_job_listings(html_file_path))
