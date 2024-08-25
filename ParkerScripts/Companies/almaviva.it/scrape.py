import sys
from selenium import webdriver
import os
from dotenv import load_dotenv

load_dotenv()
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import json
import threading

def main(filename):
    profile_folder_path = os.getenv("CHROME_PROFILE_PATH") + os.path.sep + str(threading.get_ident())
    service = Service(executable_path=r""+os.getenv("CHROME_DRIVER_PATH")+"")
    options = webdriver.ChromeOptions()
    options.add_argument(f"user-data-dir={profile_folder_path}")
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")

    driver = webdriver.Chrome(service=service, options=options)
    driver.get("file:///" + filename)

    jobs = []
    elements = driver.find_elements(By.CSS_SELECTOR, '.avlav-openposition')
    for element in elements:
        job_title = element.find_element(By.CSS_SELECTOR, '.avlav-openposition-detail h3').text.strip()
        job_url = element.find_element(By.CSS_SELECTOR, '.avlav-openposition a').get_attribute('href').strip()
        if job_title and job_url:
            jobs.append({"Job-title": job_title, "URL": job_url})

    driver.quit()

    print(json.dumps(jobs, ensure_ascii=False))

if __name__ == "__main__":
    filename = sys.argv[1]
    main(filename)
