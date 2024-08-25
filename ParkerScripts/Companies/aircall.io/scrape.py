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
from bs4 import BeautifulSoup

def scrape_jobs(file_path):
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
        soup = BeautifulSoup(driver.page_source, 'html.parser')

        job_openings = []
        job_blocks = driver.find_elements(By.CSS_SELECTOR, '.OpenPositions_Role__pW8dr')

        for job_block in job_blocks:
            title_element = job_block.find_element(By.CSS_SELECTOR, 'h3')
            url_element = job_block.find_element(By.CSS_SELECTOR, 'a[href]')

            job_openings.append({
                "Job-title": title_element.text.strip(),
                "URL": url_element.get_attribute('href')
            })

        print(json.dumps(job_openings, indent=4))

    finally:
        driver.quit()

if __name__ == "__main__":
    file_path = sys.argv[1]
    scrape_jobs(file_path)
