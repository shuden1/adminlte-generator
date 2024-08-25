import sys
from selenium import webdriver
import os
from dotenv import load_dotenv

load_dotenv()
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
import json
import shutil
import threading

def scrape_job_listings(file_name):
    job_listing_selector = ".gnewtonCareerGroupRowClass .gnewtonCareerGroupJobTitleClass a"
    profile_folder_path = os.getenv("CHROME_PROFILE_PATH") + os.path.sep + str(threading.get_ident())
    service = Service(executable_path=r""+os.getenv("CHROME_DRIVER_PATH")+"")

    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument(f"user-data-dir={profile_folder_path}")
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")

    driver = webdriver.Chrome(service=service, options=chrome_options)
    driver.get(f"file:///{file_name}")

    job_elements = driver.find_elements(By.CSS_SELECTOR, job_listing_selector)
    jobs = [{"Job-title": e.text, "URL": e.get_attribute("href")} for e in job_elements]

    driver.quit()
    # shutil.rmtree(profile_folder_path, ignore_errors=True)
    return json.dumps(jobs)

if __name__ == "__main__":
    html_file_name = sys.argv[1]
    print(scrape_job_listings(html_file_name))
