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

def scrape_jobs(file_name):
    profile_folder_path = os.getenv("CHROME_PROFILE_PATH") + os.path.sep + str(threading.get_ident())
    service = Service(executable_path=r""+os.getenv("CHROME_DRIVER_PATH")+"")

    options = Options()
    options.add_argument(f"user-data-dir={profile_folder_path}")
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")

    driver = webdriver.Chrome(service=service, options=options)

    try:
        driver.get(f"file:///{file_name}")

        job_openings = []

        # Use the selectors identified in STEP 1
        job_blocks = driver.find_elements(By.CSS_SELECTOR, 'div[class*="job"]')  # Generalized class name for job blocks

        for block in job_blocks:
            title_tag = block.find_element(By.CSS_SELECTOR, 'a[href*="job"]')  # Generalized selector for job title links
            job_title = title_tag.text.strip()
            job_url = title_tag.get_attribute('href')
            job_openings.append({"Job-title": job_title, "URL": job_url})

        print(json.dumps(job_openings, indent=4))

    finally:
        driver.quit()

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script.py <html_file_path>")
        sys.exit(1)

    file_name = sys.argv[1]
    scrape_jobs(file_name)
