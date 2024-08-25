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
    profile_folder_path = os.getenv("CHROME_PROFILE_PATH") + "\\" + str(threading.get_ident())
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
        job_blocks = driver.find_elements(By.CSS_SELECTOR, 'div.VacancyCards_cardsWrapper__1KvDe')

        for job_block in job_blocks:
            title_tags = job_block.find_elements(By.CSS_SELECTOR, 'a.VacancyCards_card__vMQTI')
            for title_tag in title_tags:
                job_title = title_tag.find_element(By.CSS_SELECTOR, 'h3.Title_title__mv7GI').text.strip()
                job_url = title_tag.get_attribute('href')
                job_openings.append({"Job-title": job_title, "URL": job_url})

        print(json.dumps(job_openings, indent=4))

    finally:
        driver.quit()

if __name__ == "__main__":
    file_path = sys.argv[1]
    scrape_jobs(file_path)
