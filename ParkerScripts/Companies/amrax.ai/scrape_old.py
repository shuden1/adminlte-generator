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

def scrape_jobs(html_file_path):
    profile_folder_path = os.getenv("CHROME_PROFILE_PATH") + os.path.sep + str(threading.get_ident())
    service = Service(executable_path=r""+os.getenv("CHROME_DRIVER_PATH")+"")

    options = Options()
    options.add_argument(f"user-data-dir={profile_folder_path}")
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")

    driver = webdriver.Chrome(service=service, options=options)

    driver.get(f"file:///{html_file_path}")

    job_openings = driver.find_elements(By.CSS_SELECTOR, "div.elementor-widget-container")

    job_listings = []

    for job_opening in job_openings:
        job_titles = job_opening.find_elements(By.CSS_SELECTOR, "a[rel='noopener'][target='_blank']")
        for job_title in job_titles:
            title = job_title.get_attribute('innerHTML').strip()
            url = job_title.get_attribute('href') or "#"
            job_listings.append({"Job-title": title, "URL": url})

    driver.quit()

    return json.dumps(job_listings, indent=4)

if __name__ == "__main__":
    html_file_path = sys.argv[1]
    print(scrape_jobs(html_file_path))
