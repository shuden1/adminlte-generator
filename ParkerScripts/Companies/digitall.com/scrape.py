import sys
from selenium import webdriver
import os
from dotenv import load_dotenv

load_dotenv()
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
import threading
import json

def crawl_job_listings(file_name):
    service = ChromeService(executable_path=r""+os.getenv("CHROME_DRIVER_PATH")+"")
    profile_folder_path=os.getenv("CHROME_PROFILE_PATH") + "\\"+str(threading.get_ident())
    options = webdriver.ChromeOptions()
    options.add_argument(f"user-data-dir={profile_folder_path}")
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")

    driver = webdriver.Chrome(service=service, options=options)
    driver.get(f"file:///{file_name}")

    job_elements = driver.find_elements(By.CSS_SELECTOR, ".listing div.card")
    job_listings = []

    for job_element in job_elements:
        title_element = job_element.find_element(By.CSS_SELECTOR, "h3 a")
        job_title = title_element.text
        job_url = title_element.get_attribute('href')
        job_listings.append({"Job-title": job_title, "URL": job_url})

    driver.quit()
    return json.dumps(job_listings)

if __name__ == "__main__":
    file_name = sys.argv[1]
    print(crawl_job_listings(file_name))
