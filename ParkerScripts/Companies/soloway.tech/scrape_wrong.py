import sys
import threading
from selenium import webdriver
import os
from dotenv import load_dotenv

load_dotenv()
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By

def main(html_file):
    profile_folder_path = os.getenv("CHROME_PROFILE_PATH") + os.path.sep + str(threading.get_ident())
    service = Service(executable_path=r""+os.getenv("CHROME_DRIVER_PATH")+"")
    options = webdriver.ChromeOptions()
    options.add_argument(f"user-data-dir={profile_folder_path}")
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")

    with webdriver.Chrome(service=service, options=options) as driver:
        driver.get(f"file:///{html_file}")
        job_listings = []
        jobs = driver.find_elements(By.CSS_SELECTOR, ".s_open_positions_item")
        for job in jobs:
            title = job.find_element(By.CSS_SELECTOR, ".s_changes_item_title").text
            url = job.find_element(By.CSS_SELECTOR, "a").get_attribute("href")
            job_listings.append({"Job-title": title, "URL": url})
    print(job_listings)

if __name__ == "__main__":
    html_file = sys.argv[1]
    main(html_file)
