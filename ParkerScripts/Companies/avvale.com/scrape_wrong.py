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

    job_blocks = driver.find_elements(By.CSS_SELECTOR, 'div[class*="jobcard"], div[class*="jobtitle"], div[class*="job"], ul[class*="job"], div[class*="career"], ul[class*="career"], div[class*="opening"], ul[class*="opening"]')
    for job_block in job_blocks:
        title_tags = job_block.find_elements(By.CSS_SELECTOR, 'a, h2, h3, h4, p')
        for title_tag in title_tags:
            job_title = title_tag.text.strip()
            job_url = title_tag.get_attribute('href')
            if job_title and job_url and 'mailto:' not in job_url:
                job_openings.append({"Job-title": job_title, "URL": job_url})

    driver.quit()

    return json.dumps(job_openings, indent=4)

if __name__ == "__main__":
    file_path = sys.argv[1]
    print(scrape_jobs(file_path))
