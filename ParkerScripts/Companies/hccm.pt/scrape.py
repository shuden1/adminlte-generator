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

    job_elements = driver.find_elements(By.CSS_SELECTOR, "div.card-hover.card.js-hover-img-link.shadow-sm.hover-lift.hover-shadow-sm.px-4.py-2.border-start-0.border-top-0.border-end-0")

    jobs = []

    for job_element in job_elements:
        title_element = job_element.find_element(By.CSS_SELECTOR, "small.d-block.fs-5.pt-1")
        url_element = job_element.find_element(By.CSS_SELECTOR, "a.d-flex.link-hover-underline.link-2x.align-items-center.justify-content-between")

        title = title_element.get_attribute('innerHTML').strip()
        url = url_element.get_attribute('href') if url_element.get_attribute('href') else "#"

        jobs.append({"Job-title": title, "URL": url})

    driver.quit()

    return json.dumps(jobs, indent=4)

if __name__ == "__main__":
    file_path = sys.argv[1]
    print(scrape_jobs(file_path))
