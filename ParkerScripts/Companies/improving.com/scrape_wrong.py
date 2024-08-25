import sys
from selenium import webdriver
import os
from dotenv import load_dotenv

load_dotenv()
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
import threading
import json

def scrape_job_listings(target_html_file):
    profile_folder_path = os.getenv("CHROME_PROFILE_PATH") + os.path.sep + str(threading.get_ident())
    service = ChromeService(executable_path=r""+os.getenv("CHROME_DRIVER_PATH")+"")
    options = webdriver.ChromeOptions()
    options.add_argument(f"user-data-dir={profile_folder_path}")
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")

    driver = webdriver.Chrome(service=service, options=options)
    driver.get(f"file:///{target_html_file}")

    job_elements = driver.find_elements(By.CSS_SELECTOR, ".MuiDataGrid-row.MuiDataGrid-row--dynamicHeight a[href]")
    job_listings = []

    for job_element in job_elements:
        job_title = job_element.text
        if job_title:  # Check if job title is not empty
            job_url = job_element.get_attribute("href")
            job_listings.append({"Job-title": job_title, "URL": job_url})

    driver.quit()

    return json.dumps(job_listings, indent=2)


if __name__ == "__main__":
    target_html_file = sys.argv[1]
    print(scrape_job_listings(target_html_file))
