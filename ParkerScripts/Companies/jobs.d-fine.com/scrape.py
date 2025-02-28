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

def scrape_jobs(html_file):
    profile_folder_path = os.getenv("CHROME_PROFILE_PATH") + os.path.sep + str(threading.get_ident())
    service = Service(executable_path=r""+os.getenv("CHROME_DRIVER_PATH")+"")

    options = Options()
    options.add_argument(f"user-data-dir={profile_folder_path}")
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")

    driver = webdriver.Chrome(service=service, options=options)

    driver.get(f"file:///{html_file}")

    job_elements = driver.find_elements(By.CSS_SELECTOR, 'a.dvinci-job-entry.card')
    jobs = []

    for job_element in job_elements:
        title_element = job_element.find_element(By.CSS_SELECTOR, 'h3.dvinci-job-position')
        title = title_element.text.strip()

        url = job_element.get_attribute('href')
        if not url:
            url = "#"

        jobs.append({"Job-title": title, "URL": url})

    driver.quit()

    return json.dumps(jobs, indent=4)

if __name__ == "__main__":
    html_file = sys.argv[1]
    print(scrape_jobs(html_file))
