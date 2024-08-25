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

def scrape_jobs(file_name):
    profile_folder_path = os.getenv("CHROME_PROFILE_PATH") + os.path.sep + str(threading.get_ident())
    service = Service(executable_path=r""+os.getenv("CHROME_DRIVER_PATH")+"")

    options = Options()
    options.add_argument(f"user-data-dir={profile_folder_path}")
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")

    driver = webdriver.Chrome(service=service, options=options)

    try:
        driver.get(f"file:///{file_name}")

        job_openings = driver.find_elements(By.CSS_SELECTOR, "li.grid.grid-cols-3.px-4.py-3.text-xs.font-semibold.first\\:rounded-t-lg.last\\:rounded-b-lg.odd\\:bg-gray-100")
        jobs = []

        for job in job_openings:
            title_element = job.find_element(By.CSS_SELECTOR, "a.w-10/12.text-xs.font-semibold.text-purple-600.hover\\:text-purple-700")
            title = title_element.get_attribute('innerHTML').strip()
            url = title_element.get_attribute('href') or "#"

            jobs.append({"Job-title": title, "URL": url})

        print(json.dumps(jobs, indent=4))

    finally:
        driver.quit()

if __name__ == "__main__":
    file_name = sys.argv[1]
    scrape_jobs(file_name)
