import sys
import json
from selenium import webdriver
import os
from dotenv import load_dotenv

load_dotenv()
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import threading

def scrape_job_listings(filepath):
    chrome_options = Options()
    profile_path = os.getenv("CHROME_PROFILE_PATH") + "\\" + str(threading.get_ident())
    chrome_options.add_argument(f"user-data-dir={profile_path}")
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")

    service = Service(executable_path=r""+os.getenv("CHROME_DRIVER_PATH")+"")
    driver = webdriver.Chrome(service=service, options=chrome_options)

    driver.get(f"file:///{filepath}")
    jobs = []

    job_elements = driver.find_elements(By.CSS_SELECTOR, ".career-list__item")

    for job_element in job_elements:
        title_element = job_element.find_element(By.CSS_SELECTOR, "a")
        title = title_element.text
        url = title_element.get_attribute('href')
        if title.lower() != "read more":
            jobs.append({"Job-title": title, "URL": url})

    driver.quit()

    return json.dumps(jobs, indent=2)

if __name__ == "__main__":
    filepath = sys.argv[1]
    print(scrape_job_listings(filepath))
