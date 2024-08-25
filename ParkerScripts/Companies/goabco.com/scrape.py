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

def scrape_jobs(html_file_path):
    profile_folder_path = os.getenv("CHROME_PROFILE_PATH") + os.path.sep + str(threading.get_ident())
    service = Service(executable_path=r""+os.getenv("CHROME_DRIVER_PATH")+"")

    options = webdriver.ChromeOptions()
    options.add_argument(f"user-data-dir={profile_folder_path}")
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")

    driver = webdriver.Chrome(service=service, options=options)

    try:
        driver.get(f"file:///{html_file_path}")

        job_openings = []

        job_elements = driver.find_elements(By.CSS_SELECTOR, "div.elements-div-content_section-3-module-6.general-shadow-2.aos-init.aos-animate")

        for job_element in job_elements:
            try:
                title_element = job_element.find_element(By.CSS_SELECTOR, "h3.elements--jobs__title")
                title = title_element.text.strip() or title_element.get_attribute('innerHTML').strip()
            except NoSuchElementException:
                title = "No Title"

            try:
                url_element = job_element.find_element(By.CSS_SELECTOR, "a.business--jobs__link")
                url = url_element.get_attribute('href').strip()
            except NoSuchElementException:
                url = "#"

            job_openings.append({"Job-title": title, "URL": url})

    finally:
        driver.quit()

    return json.dumps(job_openings, indent=4)

if __name__ == "__main__":
    html_file_path = sys.argv[1]
    print(scrape_jobs(html_file_path))
