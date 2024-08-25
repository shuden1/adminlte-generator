from selenium import webdriver
import os
from dotenv import load_dotenv

load_dotenv()
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import threading
import shutil
import sys
import json

def scrape_jobs(html_path):
    profile_folder_path = os.getenv("CHROME_PROFILE_PATH") + os.path.sep + str(threading.get_ident())
    options = Options()
    options.add_argument(f"user-data-dir={profile_folder_path}")
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")

    service = ChromeService(executable_path=r""+os.getenv("CHROME_DRIVER_PATH")+"")
    driver = webdriver.Chrome(service=service, options=options)
    driver.get(f"file://{html_path}")

    try:
        jobs = []
        job_elements = driver.find_elements(By.CSS_SELECTOR, "table[id='currentJobOpeningsList'] tr:not(.headerRow)")
        for job_element in job_elements:
            title_element = job_element.find_element(By.CSS_SELECTOR, "td div.jobTitle")
            title = title_element.text.strip()
            link = title_element.find_element(By.TAG_NAME, "a").get_attribute("href").strip()
            jobs.append({"Job-title": title, "URL": link})

        return json.dumps(jobs)
    finally:
        driver.quit()
        if os.path.exists(profile_folder_path):


if __name__ == "__main__":
    html_file_path = sys.argv[1]
    print(scrape_jobs(html_file_path))
