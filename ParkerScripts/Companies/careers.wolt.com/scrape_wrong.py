import sys
from selenium import webdriver
import os
from dotenv import load_dotenv

load_dotenv()
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
import threading
import json

def scrape_jobs(target_html_file):
    service = ChromeService(executable_path=r""+os.getenv("CHROME_DRIVER_PATH")+"")
    profile_folder_path = f"D:\\Mind\\CRA\\AI_Experiments\\Job_Crawlers\\Peter\\adminlte-generator\\chrome_profile\\{threading.get_ident()}"
    options = webdriver.ChromeOptions()
    options.add_argument(f"user-data-dir={profile_folder_path}")
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")

    driver = webdriver.Chrome(service=service, options=options)
    driver.get(f"file:///{target_html_file}")

    job_elements = driver.find_elements(By.CSS_SELECTOR, ".job-listing-item")
    jobs = []

    for job_element in job_elements:
        title_element = job_element.find_element(By.CSS_SELECTOR, ".job-title")
        job_title = title_element.text.strip()
        job_url = job_element.find_element(By.CSS_SELECTOR, "a").get_attribute('href').strip()
        jobs.append({"Job-title": job_title, "URL": job_url})

    driver.quit()
    return json.dumps(jobs)

if __name__ == "__main__":
    target_html_file = sys.argv[1]
    print(scrape_jobs(target_html_file))
