import sys
import json
import threading
from selenium import webdriver
import os
from dotenv import load_dotenv

load_dotenv()
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException

def scrape_jobs(file_name):
    profile_folder_path = os.getenv("CHROME_PROFILE_PATH") + "\\" + str(threading.get_ident())
    service = Service(executable_path=r""+os.getenv("CHROME_DRIVER_PATH")+"")
    options = webdriver.ChromeOptions()
    options.add_argument(f"user-data-dir={profile_folder_path}")
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")

    driver = webdriver.Chrome(service=service, options=options)
    driver.get(f"file:///{file_name}")

    job_listings = []

    try:
        job_elements = driver.find_elements(By.CSS_SELECTOR, "div.sqs-block-button-container.sqs-block-button-container--center[data-alignment='center'][data-animation-role='button'][data-button-size='medium'][data-button-type='primary']")
        for job_element in job_elements:
            try:
                title_element = job_element.find_element(By.CSS_SELECTOR, "a.sqs-block-button-element--medium.sqs-button-element--primary.sqs-block-button-element[data-initialized='true']")
                job_title = title_element.text.strip() if title_element.text.strip() else title_element.get_attribute('innerHTML').strip()
                job_url = title_element.get_attribute('href') if title_element.get_attribute('href') else "#"
                job_listings.append({"Job-title": job_title, "URL": job_url})
            except NoSuchElementException:
                continue
    except NoSuchElementException:
        pass

    driver.quit()
    return json.dumps(job_listings, indent=4)

if __name__ == "__main__":
    file_name = sys.argv[1]
    print(scrape_jobs(file_name))
