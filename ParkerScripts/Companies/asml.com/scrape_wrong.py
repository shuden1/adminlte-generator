import sys
from selenium import webdriver
import os
from dotenv import load_dotenv

load_dotenv()
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import threading
import json

def scrape_job_listings(html_file_name):
    profile_folder_path = os.getenv("CHROME_PROFILE_PATH") + os.path.sep + str(threading.get_ident())
    service = Service(executable_path=r""+os.getenv("CHROME_DRIVER_PATH")+"")
    options = webdriver.ChromeOptions()
    options.add_argument(f"user-data-dir={profile_folder_path}")
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")

    driver = webdriver.Chrome(service=service, options=options)
    driver.get(f"file:///{html_file_name}")

    job_listings = []
    job_blocks = driver.find_elements(By.CSS_SELECTOR, ".job-opening-block")
    for block in job_blocks:
        job_title_elements = block.find_elements(By.CSS_SELECTOR, ".job-title")
        job_url_elements = block.find_elements(By.CSS_SELECTOR, "a")
        for title_element, url_element in zip(job_title_elements, job_url_functions):
            job_title = title_element.text
            job_url = url_element.get_attribute('href')
            job_listings.append({"Job-title": job_title, "URL": job_url})

    driver.quit()
    return json.dumps(job_listings)

if __name__ == "__main__":
    html_file_name = sys.argv[1]
    print(scrape_job_listings(html_file_name))
