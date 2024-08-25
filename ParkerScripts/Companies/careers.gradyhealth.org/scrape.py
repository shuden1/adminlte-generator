from selenium import webdriver
import os
from dotenv import load_dotenv

load_dotenv()
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
import threading
import sys
import json

def scrape_jobs(target_html_file):
    profile_folder_path = os.getenv("CHROME_PROFILE_PATH") + "\\" + str(threading.get_ident())
    service = Service(executable_path=r""+os.getenv("CHROME_DRIVER_PATH")+"")
    options = webdriver.ChromeOptions()
    options.add_argument(f"user-data-dir={profile_folder_path}")
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")

    driver = webdriver.Chrome(service=service, options=options)
    driver.get(f"file:///{target_html_file}")

    job_elements = driver.find_elements(By.CSS_SELECTOR, "div.list-group-item.border-left-0.border-right-0.px-0.py-4.ng-star-inserted")
    job_listings = []
    for job_element in job_elements:
        title = job_element.find_element(By.CSS_SELECTOR, "a").text
        url = job_element.find_element(By.CSS_SELECTOR, "a").get_attribute("href")
        job_listings.append({"Job-title": title, "URL": url})

    driver.quit()
    return json.dumps(job_listings)

if __name__ == "__main__":
    target_html_file = sys.argv[1]
    result = scrape_jobs(target_html_file)
    print(result)
