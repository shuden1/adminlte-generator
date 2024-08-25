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

    try:
        driver.get(f"file:///{file_path}")

        job_openings = driver.find_elements(By.CSS_SELECTOR, "div.fs-12.fs-l-8.fs-xl-9.padding-left-l-20")
        job_listings = []

        for job_opening in job_openings:
            try:
                job_title_element = job_opening.find_element(By.CSS_SELECTOR, "h2.heading-3.job-list-sr--item-title")
                job_title = job_title_element.text.strip() or job_title_element.get_attribute('innerHTML').strip()
            except NoSuchElementException:
                job_title = "No Title"

            try:
                job_url_element = job_opening.find_element(By.CSS_SELECTOR, "a.job-list-sr--link")
                job_url = job_url_element.get_attribute('href') or "#"
            except NoSuchElementException:
                job_url = "#"

            job_listings.append({"Job-title": job_title, "URL": job_url})

    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        driver.quit()

    return json.dumps(job_listings, indent=4)

if __name__ == "__main__":
    file_path = sys.argv[1]
    print(scrape_jobs(file_path))
