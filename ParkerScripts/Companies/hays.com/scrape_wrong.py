import sys
from selenium import webdriver
import os
from dotenv import load_dotenv

load_dotenv()
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
import threading
import json

def scrape_job_listings(file_path):
    service = Service(executable_path=r""+os.getenv("CHROME_DRIVER_PATH")+"")
    options = webdriver.ChromeOptions()
    profile_path = os.getenv("CHROME_PROFILE_PATH") + os.path.sep + str(threading.get_ident())
    options.add_argument(f"user-data-dir={profile_path}")
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")

    driver = webdriver.Chrome(service=service, options=options)
    driver.get(file_path)

    # Assuming job listings are within <a> tags. Please replace `.job-listing` and `.job-title` with actual selectors identified in step 1
    job_elements = driver.find_elements(By.CSS_SELECTOR, "a")  # Placeholder selector
    jobs = [{"Job-title": e.text, "URL": e.get_attribute('href')} for e in job_elements if e.text and e.get_attribute('href')]

    driver.quit()

    return json.dumps(jobs)

if __name__ == "__main__":
    file_path = sys.argv[1]  # The script expects the file path as the first argument
    print(scrape_job_listings(file_path))
