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
    service = Service(executable_path=r"C:\\Python3\\chromedriver.exe")

    options = Options()
    options.add_argument(f"user-data-dir={profile_folder_path}")
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")

    driver = webdriver.Chrome(service=service, options=options)

    driver.get(f"file:///{file_path}")

    job_openings = []

    # Assuming job listings are in a <div> with class 'cc-row__content'
    job_blocks = driver.find_elements(By.CSS_SELECTOR, 'div.cc-row__content')

    for block in job_blocks:
        # Assuming job titles are in <a> tags within the job blocks
        title_tags = block.find_elements(By.CSS_SELECTOR, 'a')
        for title_tag in title_tags:
            job_title = title_tag.text.strip()
            job_url = title_tag.get_attribute('href')
            if job_title and job_url:
                job_openings.append({"Job-title": job_title, "URL": job_url})

    driver.quit()

    return json.dumps(job_openings, indent=4)

if __name__ == "__main__":
    file_path = sys.argv[1]
    print(scrape_jobs(file_path))
