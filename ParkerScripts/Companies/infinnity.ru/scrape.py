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
from selenium.common.exceptions import NoSuchElementException

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

        job_openings = []

        job_elements = driver.find_elements(By.CSS_SELECTOR, 'a.vacancies__card')

        for job_element in job_elements:
            try:
                title_element = job_element.find_element(By.CSS_SELECTOR, 'span.vacancies__title')
                job_title = title_element.text.strip() or title_element.get_attribute('innerHTML').strip()
            except NoSuchElementException:
                job_title = "No Title"

            job_url = job_element.get_attribute('href') or "#"

            job_openings.append({"Job-title": job_title, "URL": job_url})

    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        driver.quit()

    return json.dumps(job_openings, ensure_ascii=False)

if __name__ == "__main__":
    file_path = sys.argv[1]
    print(scrape_job_listings(file_path))
