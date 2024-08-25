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

def scrape_jobs(html_file_path):
    profile_folder_path = os.getenv("CHROME_PROFILE_PATH") + "\\" + str(threading.get_ident())
    service = Service(executable_path=r""+os.getenv("CHROME_DRIVER_PATH")+"")

    options = Options()
    options.add_argument(f"user-data-dir={profile_folder_path}")
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")

    driver = webdriver.Chrome(service=service, options=options)

    driver.get(f"file:///{html_file_path}")

    job_listings = driver.find_elements(By.CSS_SELECTOR, 'li.job-card')

    jobs = []
    for job in job_listings:
        try:
            title_element = job.find_element(By.CSS_SELECTOR, 'div.title h3')
            url_element = job.find_element(By.CSS_SELECTOR, 'div.link a')

            job_title = title_element.text
            job_url = url_element.get_attribute('href')

            if job_title and job_url:
                jobs.append({"Job-title": job_title, "URL": job_url})
        except Exception as e:
            continue

    driver.quit()

    return json.dumps(jobs, indent=4)

if __name__ == "__main__":
    html_file_path = sys.argv[1]
    print(scrape_jobs(html_file_path))
