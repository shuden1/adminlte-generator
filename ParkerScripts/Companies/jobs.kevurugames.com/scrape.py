import sys
from selenium import webdriver
import os
from dotenv import load_dotenv

load_dotenv()
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
import json
import threading

def scrape_job_listings(html_file_path):
    profile_folder_path = os.getenv("CHROME_PROFILE_PATH") + os.path.sep + str(threading.get_ident())
    service = ChromeService(executable_path=r""+os.getenv("CHROME_DRIVER_PATH")+"")
    options = webdriver.ChromeOptions()
    options.add_argument(f"user-data-dir={profile_folder_path}")
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")

    driver = webdriver.Chrome(service=service, options=options)
    driver.get(f"file:///{html_file_path}")

    job_listings = []
    jobs = driver.find_elements(By.CSS_SELECTOR, ".st_vacancy")
    for job in jobs:
        title_element = job.find_element(By.CSS_SELECTOR, ".st_vacancy_name")
        url_element = job.find_element(By.CSS_SELECTOR, ".st_vacancy_more")
        job_listings.append({
            "Job-title": title_element.text,
            "URL": url_element.get_attribute("href")
        })

    driver.quit()
    return json.dumps(job_listings)

if __name__ == "__main__":
    html_file_path = sys.argv[1]
    print(scrape_job_listings(html_file_path))
