import sys
import json
import threading
from selenium import webdriver
import os
from dotenv import load_dotenv

load_dotenv()
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

def scrape_jobs(file_path):
    profile_folder_path = os.getenv("CHROME_PROFILE_PATH") + "\\" + str(threading.get_ident())
    service = Service(executable_path=r""+os.getenv("CHROME_DRIVER_PATH")+"")

    options = Options()
    options.add_argument(f"user-data-dir={profile_folder_path}")
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")

    driver = webdriver.Chrome(service=service, options=options)

    driver.get(f"file:///{file_path}")

    job_openings = []

    # Use the selectors defined in STEP 1 to find job listings
    job_blocks = driver.find_elements(By.CSS_SELECTOR, 'div[class*="job"]')
    for job in job_blocks:
        title_tag = job.find_element(By.CSS_SELECTOR, 'a')
        title = title_tag.text
        url = title_tag.get_attribute('href')
        job_openings.append({"Job-title": title, "URL": url})

    driver.quit()

    return json.dumps(job_openings, ensure_ascii=False)

if __name__ == "__main__":
    file_path = sys.argv[1]
    job_listings = scrape_jobs(file_path)
    print(job_listings)
