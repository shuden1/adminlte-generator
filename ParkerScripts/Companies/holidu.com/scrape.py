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

def scrape_jobs(html_file_path):
    profile_folder_path = os.getenv("CHROME_PROFILE_PATH") + "\\" + str(threading.get_ident())
    service = Service(executable_path=r""+os.getenv("CHROME_DRIVER_PATH")+"")

    options = Options()
    options.add_argument(f"user-data-dir={profile_folder_path}")
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")

    driver = webdriver.Chrome(service=service, options=options)

    try:
        driver.get(f"file:///{html_file_path}")

        job_openings = []
        job_blocks = driver.find_elements(By.CSS_SELECTOR, 'a.text-black-ultra')

        for job_block in job_blocks:
            title_tag = job_block.find_element(By.CSS_SELECTOR, 'h3')
            if title_tag:
                title = title_tag.text.strip()
                url = job_block.get_attribute('href')
                job_openings.append({"Job-title": title, "URL": url})

        print(json.dumps(job_openings, indent=4))

    finally:
        driver.quit()

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script.py <html_file_path>")
        sys.exit(1)

    html_file_path = sys.argv[1]
    scrape_jobs(html_file_path)
