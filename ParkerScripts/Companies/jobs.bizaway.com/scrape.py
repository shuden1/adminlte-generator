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

    job_opening_selector = '.list-group-item'
    job_title_selector = '.list-group-item-heading a'
    job_url_selector = '.list-group-item-heading a'

    job_elements = driver.find_elements(By.CSS_SELECTOR, job_opening_selector)

    job_postings = []
    for job_element in job_elements:
        title_element = job_element.find_element(By.CSS_SELECTOR, job_title_selector)
        title = title_element.text
        url = title_element.get_attribute('href')
        job_postings.append({"Job-title": title, "URL": url})

    driver.quit()

    return json.dumps(job_postings, indent=4)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script.py <path_to_html_file>")
        sys.exit(1)

    file_path = sys.argv[1]
    job_postings_json = scrape_jobs(file_path)
    print(job_postings_json)
