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
from selenium.common.exceptions import NoSuchElementException

def scrape_jobs(html_file):
    profile_folder_path = os.getenv("CHROME_PROFILE_PATH") + os.path.sep + str(threading.get_ident())

    options = Options()
    options.add_argument(f"user-data-dir={profile_folder_path}")
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")

    service = ChromeService(executable_path=r""+os.getenv("CHROME_DRIVER_PATH")+"")

    driver = webdriver.Chrome(service=service, options=options)

    driver.get(f"file://{html_file}")

    job_listings = []

    try:
        job_elements = driver.find_elements(By.CSS_SELECTOR, "li.list-group-item")

        for job in job_elements:
            try:
                title_element = job.find_element(By.CSS_SELECTOR, "h4.list-group-item-heading a")
                title = title_element.text.strip() or title_element.get_attribute('innerHTML').strip()
                url = title_element.get_attribute('href') or "#"

                job_listings.append({"Job-title": title, "URL": url})
            except NoSuchElementException:
                continue
    except NoSuchElementException:
        pass

    driver.quit()

    return json.dumps(job_listings)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit(1)

    html_file = sys.argv[1]
    result = scrape_jobs(html_file)
    print(result)
