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

def scrape_job_listings(file_path):
    profile_folder_path = os.getenv("CHROME_PROFILE_PATH") + os.path.sep + str(threading.get_ident())
    service = Service(executable_path=r""+os.getenv("CHROME_DRIVER_PATH")+"")

    options = Options()
    options.add_argument(f"user-data-dir={profile_folder_path}")
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")

    driver = webdriver.Chrome(service=service, options=options)

    driver.get(f"file:///{file_path}")

    job_openings = []
    job_blocks = driver.find_elements(By.CSS_SELECTOR, 'div.max-w-small.desktop\\:max-w-container.mx-auto.px-0.pb-4.desktop\\:px-\\[12rem\\].desktop\\:pt-10.desktop\\:pb-20.desktop\\:grid.desktop\\:grid-cols-\\[1fr_3fr\\].gap-12')

    for job_block in job_blocks:
        job_title_tag = job_block.find_element(By.CSS_SELECTOR, 'a')
        if job_title_tag:
            job_title = job_title_tag.text.strip().split('\n')[0]  # Extract the first line as the job title
            job_url = job_title_tag.get_attribute('href')
            job_openings.append({"Job-title": job_title, "URL": job_url})

    driver.quit()

    return json.dumps(job_openings, indent=4)

if __name__ == "__main__":
    file_path = sys.argv[1]
    job_listings_json = scrape_job_listings(file_path)
    print(job_listings_json)
