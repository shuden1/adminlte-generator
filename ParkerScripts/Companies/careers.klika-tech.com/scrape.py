from selenium import webdriver
import os
from dotenv import load_dotenv

load_dotenv()
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
import threading, sys, json

def scrape_jobs(target_html_file):
    profile_folder_path = f"{os.getenv("CHROME_PROFILE_PATH")}{os.path.sep}{threading.get_ident()}"
    service = ChromeService(executable_path=r""+os.getenv("CHROME_DRIVER_PATH")+"")
    options = webdriver.ChromeOptions()
    options.add_argument(f"user-data-dir={profile_folder_path}")
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")

    with webdriver.Chrome(service=service, options=options) as driver:
        driver.get(target_html_file)
        job_elements = driver.find_elements(By.CSS_SELECTOR, ".vacancy-list__items li a.job-post__parent")
        jobs_data = []

        for job_element in job_elements:
            job_title = job_element.find_element(By.CSS_SELECTOR, "div.job-post__title h5").text
            job_url = job_element.get_attribute("href")
            jobs_data.append({"Job-title": job_title, "URL": job_url})

    print(json.dumps(jobs_data))

if __name__ == "__main__":
    target_html_file = sys.argv[1]
    scrape_jobs(target_html_file)
