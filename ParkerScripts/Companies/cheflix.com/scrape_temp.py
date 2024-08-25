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

    job_opening_selector = 'section.elementor-section.elementor-top-section.elementor-element'
    job_title_selector = 'h2.elementor-heading-title.elementor-size-default'
    job_url_selector = 'a'

    job_elements = driver.find_elements(By.CSS_SELECTOR, job_opening_selector)

    job_listings = []
    for job in job_elements:
        title_element = job.find_element(By.CSS_SELECTOR, job_title_selector)
        url_element = job.find_element(By.CSS_SELECTOR, job_url_selector)
        title = title_element.text
        url = url_element.get_attribute('href')
        job_listings.append({"Job-title": title, "URL": url})

    driver.quit()

    return json.dumps(job_listings, ensure_ascii=False)

if __name__ == "__main__":
    file_path = sys.argv[1]
    print(scrape_jobs(file_path))
