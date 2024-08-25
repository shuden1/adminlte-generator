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

def scrape_jobs(html_file_path):
    profile_folder_path = os.getenv("CHROME_PROFILE_PATH") + os.path.sep + str(threading.get_ident())
    service = Service(executable_path=r""+os.getenv("CHROME_DRIVER_PATH")+"")

    options = webdriver.ChromeOptions()
    options.add_argument(f"user-data-dir={profile_folder_path}")
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")

    driver = webdriver.Chrome(service=service, options=options)

    try:
        driver.get(f"file:///{html_file_path}")

        job_openings = driver.find_elements(By.CSS_SELECTOR, 'h3.article__header__text__title.title.title--07')
        jobs = []

        for job in job_openings:
            try:
                job_title_element = job.find_element(By.CSS_SELECTOR, 'a.link')
                job_title = job_title_element.text.strip() or job_title_element.get_attribute('innerHTML').strip()
                job_url = job_title_element.get_attribute('href') or "#"

                jobs.append({"Job-title": job_title, "URL": job_url})
            except NoSuchElementException:
                continue

        print(json.dumps(jobs, indent=4))

    except Exception as e:
        print(f"An error occurred: {e}")

    finally:
        driver.quit()

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script.py <html_file_path>")
        sys.exit(1)

    html_file_path = sys.argv[1]
    scrape_jobs(html_file_path)
