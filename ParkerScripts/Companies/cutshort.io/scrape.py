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

def scrape_jobs(file_path):
    profile_folder_path = os.getenv("CHROME_PROFILE_PATH") + os.path.sep + str(threading.get_ident())
    service = Service(executable_path=r""+os.getenv("CHROME_DRIVER_PATH")+"")

    options = Options()
    options.add_argument(f"user-data-dir={profile_folder_path}")
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")

    driver = webdriver.Chrome(service=service, options=options)

    driver.get(f"file:///{file_path}")

    job_postings = []

    job_blocks = driver.find_elements(By.CSS_SELECTOR, 'section.sc-75cc12cd-7.fNVywo div.sc-f0240f53-13.jZUANI')
    for job_block in job_blocks:
        job_title_element = job_block.find_element(By.CSS_SELECTOR, 'h3.sc-b6704a4e-0.sc-b6704a4e-1.iZCtvJ.hUfTcC')
        job_url_element = job_block.find_element(By.CSS_SELECTOR, 'a.sc-89b45c2f-0.sc-89b45c2f-1.cCGhbz.elYchA.sc-f0240f53-14.dGrFJK')

        job_title = job_title_element.text.strip()
        job_url = job_url_element.get_attribute('href')

        job_postings.append({"Job-title": job_title, "URL": job_url})

    driver.quit()

    return json.dumps(job_postings, indent=4)

if __name__ == "__main__":
    file_path = sys.argv[1]
    job_postings_json = scrape_jobs(file_path)
    print(job_postings_json)
