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

def scrape_jobs(file_path):
    profile_folder_path = os.getenv("CHROME_PROFILE_PATH") + os.path.sep + str(threading.get_ident())
    service = Service(executable_path=r""+os.getenv("CHROME_DRIVER_PATH")+"")

    options = webdriver.ChromeOptions()
    options.add_argument(f"user-data-dir={profile_folder_path}")
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")

    driver = webdriver.Chrome(service=service, options=options)

    try:
        driver.get(f"file:///{file_path}")

        job_listings = []

        job_opening_elements = driver.find_elements(By.CSS_SELECTOR, 'a[href="jobs/vakansya-java-razrabotchik-izhevsk"], h3.tn-atom[field="tn_text_1614500504712"]')

        for job_element in job_opening_elements:
            try:
                job_title = job_element.text.strip()
                if not job_title:
                    job_title = job_element.get_attribute('innerHTML').strip()

                job_url = job_element.get_attribute('href') if job_element.tag_name == 'a' else "#"

                job_listings.append({"Job-title": job_title, "URL": job_url})
            except NoSuchElementException:
                continue

        print(json.dumps(job_listings, ensure_ascii=False))

    finally:
        driver.quit()

if __name__ == "__main__":
    file_path = sys.argv[1]
    scrape_jobs(file_path)
