from selenium import webdriver
import os
from dotenv import load_dotenv

load_dotenv()
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import threading
import shutil
import sys
import json

def main(html_file):
    profile_folder_path = os.getenv("CHROME_PROFILE_PATH") + "\\" + str(threading.get_ident())

    service = Service(executable_path=r""+os.getenv("CHROME_DRIVER_PATH")+"")
    options = webdriver.ChromeOptions()
    options.add_argument(f"user-data-dir={profile_folder_path}")
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")

    driver = webdriver.Chrome(service=service, options=options)
    driver.get(f"file:///{html_file}")

    job_listings = []
    for job_element in driver.find_elements(By.CSS_SELECTOR, '.article--result'):
        title_element = job_element.find_element(By.CSS_SELECTOR, '.article__header__text__title--2 a')
        job_title = title_element.text
        job_url = title_element.get_attribute('href')
        job_listings.append({"Job-title": job_title, "URL": job_url})

    driver.quit()
    # shutil.rmtree(profile_folder_path, ignore_errors=True)

    return json.dumps(job_listings)

if __name__ == "__main__":
    html_file_path = sys.argv[1]
    print(main(html_file_path))
