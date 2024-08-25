import sys
import json
import threading
from selenium import webdriver
import os
from dotenv import load_dotenv

load_dotenv()
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
import time

def scrape_jobs(html_file):
    profile_folder_path = f"{os.getenv("CHROME_PROFILE_PATH")}{os.path.sep}{threading.get_ident()}"

    options = Options()
    options.add_argument(f"user-data-dir={profile_folder_path}")
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")

    service = ChromeService(executable_path=r""+os.getenv("CHROME_DRIVER_PATH")+"")

    driver = webdriver.Chrome(service=service, options=options)

    try:
        driver.get(f"file://{html_file}")

        # Click on the select element and choose "Most recent"
        select_element = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "sortselect"))
        )
        select_element.click()

        option = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "#sortselect option[value='Most recent']"))
        )
        option.click()

        # Wait for the page to update
        time.sleep(5)

        # Scrape job listings
        job_listings = driver.find_elements(By.CSS_SELECTOR, "li.jobs-list-item[data-ph-at-id='jobs-list-item'][role='listitem']")

        jobs = []
        for job in job_listings:
            try:
                title_element = job.find_element(By.CSS_SELECTOR, "span[data-ph-id='ph-page-element-page15-JAanBI']")
                title = title_element.text.strip() or title_element.get_attribute('innerHTML').strip()

                url_element = job.find_element(By.CSS_SELECTOR, "a[data-ph-at-id='job-link']")
                url = url_element.get_attribute('href') or "#"

                jobs.append({"Job-title": title, "URL": url})
            except NoSuchElementException:
                continue

        return json.dumps(jobs)

    finally:
        driver.quit()

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script.py <path_to_html_file>")
        sys.exit(1)

    html_file = sys.argv[1]
    result = scrape_jobs(html_file)
    print(result)
