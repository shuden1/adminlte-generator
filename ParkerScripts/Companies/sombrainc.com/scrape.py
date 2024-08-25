from selenium import webdriver
import os
from dotenv import load_dotenv

load_dotenv()
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
import json
import sys
import threading

def scrape_jobs(target_html_file):
    # STEP 2: Selenium setup with headless Chrome
    profile_folder_path = os.getenv("CHROME_PROFILE_PATH") + "\\" + str(threading.get_ident())
    service = ChromeService(executable_path=r""+os.getenv("CHROME_DRIVER_PATH")+"")
    options = webdriver.ChromeOptions()
    options.add_argument(f"user-data-dir={profile_folder_path}")
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")

    driver = webdriver.Chrome(service=service, options=options)
    driver.get(f"file:///{target_html_file}")

    # Using defined selectors from STEP 1
    job_blocks_selector = ".CareersList_careers__container__mSZtz .Vacancy_card__5W0_P"
    job_title_selector = ".Vacancy_card__title__Wn7_e"
    url_attribute = "href"

    jobs = driver.find_elements(By.CSS_SELECTOR, job_blocks_selector)
    results = []
    for job in jobs:
        title = job.find_element(By.CSS_SELECTOR, job_title_selector).text
        url = job.get_attribute(url_attribute)
        results.append({"Job-title": title, "URL": url})

    driver.quit()
    return json.dumps(results)

if __name__ == "__main__":
    target_html_file = sys.argv[1]
    print(scrape_jobs(target_html_file))
