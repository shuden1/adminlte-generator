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
from selenium.webdriver.chrome.options import Options

def scrape_job_listings(file_path):
    profile_folder_path = os.getenv("CHROME_PROFILE_PATH") + os.path.sep + str(threading.get_ident())
    service = Service(executable_path=r""+os.getenv("CHROME_DRIVER_PATH")+"")

    options = Options()
    options.add_argument(f"user-data-dir={profile_folder_path}")
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")

    driver = webdriver.Chrome(service=service, options=options)

    try:
        driver.get(f"file:///{file_path}")

        job_listings = []
        job_elements = driver.find_elements(By.CSS_SELECTOR, "div.entry-content")

        for job_element in job_elements:
            try:
                title_element = job_element.find_element(By.CSS_SELECTOR, "h3")
                job_title = title_element.text.strip() or title_element.get_attribute('innerHTML').strip()
            except NoSuchElementException:
                job_title = "No Title Found"

            job_url = "#"

            job_listings.append({"Job-title": job_title, "URL": job_url})

        print(json.dumps(job_listings, indent=4))

    except Exception as e:
        print(f"An error occurred: {e}")

    finally:
        driver.quit()

if __name__ == "__main__":
    file_path = sys.argv[1]
    scrape_job_listings(file_path)
