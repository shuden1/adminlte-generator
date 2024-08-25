import sys
import json
import threading
from selenium import webdriver
import os
from dotenv import load_dotenv

load_dotenv()
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException

def scrape_job_postings(file_path):
    profile_folder_path = os.getenv("CHROME_PROFILE_PATH") + os.path.sep + str(threading.get_ident())
    service = Service(executable_path=r""+os.getenv("CHROME_DRIVER_PATH")+"")
    options = webdriver.ChromeOptions()
    options.add_argument(f"user-data-dir={profile_folder_path}")
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")

    driver = webdriver.Chrome(service=service, options=options)
    driver.get(f"file:///{file_path}")

    job_postings = []

    try:
        job_elements = driver.find_elements(By.CSS_SELECTOR, "div.views-row")
        for job_element in job_elements:
            try:
                title_element = job_element.find_element(By.CSS_SELECTOR, "div.row-title a")
                job_title = title_element.text.strip() or title_element.get_attribute('innerHTML').strip()
                job_url = title_element.get_attribute('href') or "#"
                job_postings.append({"Job-title": job_title, "URL": job_url})
            except NoSuchElementException:
                continue
    except NoSuchElementException:
        pass

    driver.quit()
    return json.dumps(job_postings, indent=4)

if __name__ == "__main__":
    file_path = sys.argv[1]
    print(scrape_job_postings(file_path))
