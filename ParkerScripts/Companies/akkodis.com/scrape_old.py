import sys
import json
import threading
from selenium import webdriver
import os
from dotenv import load_dotenv

load_dotenv()
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By

def scrape_job_listings(html_file):
    profile_folder_path = os.getenv("CHROME_PROFILE_PATH") + os.path.sep + str(threading.get_ident())
    service = ChromeService(executable_path=r""+os.getenv("CHROME_DRIVER_PATH")+"")
    options = webdriver.ChromeOptions()
    options.add_argument(f"user-data-dir={profile_folder_path}")
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")

    driver = webdriver.Chrome(service=service, options=options)
    driver.get(f"file:///{html_file}")

    job_listings = []
    # Adjusted the selector based on feedback and careful review
    job_titles = driver.find_elements(By.CSS_SELECTOR, 'a[href*="/careers/jobs/"]')
    for job_title in job_titles:
        title = job_title.text.strip()
        url = job_title.get_attribute('href').strip()
        if title and url:  # Ensure both title and URL are not empty
            job_listings.append({"Job-title": title, "URL": url})

    driver.quit()
    return json.dumps(job_listings)

if __name__ == "__main__":
    html_file_path = sys.argv[1]
    print(scrape_job_listings(html_file_path))
