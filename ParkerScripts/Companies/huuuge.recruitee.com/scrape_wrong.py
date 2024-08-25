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
    service = Service(executable_path=r"C:\\Python3\\chromedriver.exe")

    options = Options()
    options.add_argument(f"user-data-dir={profile_folder_path}")
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")

    driver = webdriver.Chrome(service=service, options=options)

    driver.get(f"file:///{file_path}")

    job_data = []

    job_blocks = driver.find_elements(By.CSS_SELECTOR, 'div[data-component="PublicApp"] div[data-props*="offers"] div[class*="job"]')  # Adjusted selector to target job blocks
    for job_block in job_blocks:
        job_title_tag = job_block.find_element(By.CSS_SELECTOR, 'a[href*="offers"]')  # Adjusted selector to target job titles and URLs
        job_title = job_title_tag.text
        job_url = job_title_tag.get_attribute('href')
        job_data.append({"Job-title": job_title, "URL": job_url})

    driver.quit()

    return json.dumps(job_data, indent=4)

if __name__ == "__main__":
    file_path = sys.argv[1]
    print(scrape_jobs(file_path))
