import sys
from selenium import webdriver
import os
from dotenv import load_dotenv

load_dotenv()
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
import threading
import json

def main():
    html_file_path = sys.argv[1]
    profile_folder_path = f"{os.getenv("CHROME_PROFILE_PATH")}{os.path.sep}{threading.get_ident()}"

    service = Service(executable_path=r"C:\\Python3\\chromedriver.exe")
    options = webdriver.ChromeOptions()
    options.add_experimental_option("excludeSwitches", ["enable-logging"])  # Suppressing irrelevant log messages
    options.add_argument(f"user-data-dir={profile_folder_path}")
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")

    driver = webdriver.Chrome(service=service, options=options)
    driver.get(f"file:///{html_file_path}")

    job_elements = driver.find_elements(By.CSS_SELECTOR, "article.job, .job-posting, .job-listing")
    jobs_json = []

    for element in job_elements:
        title_element = element.find_element(By.CSS_SELECTOR, "h2, .job-title")
        url_element = element.find_element(By.CSS_SELECTOR, "a")

        job_title = title_element.text
        job_url = url_element.get_attribute("href")

        jobs_json.append({"Job-title": job_title, "URL": job41

    driver.quit()

    print(json.dumps(jobs_json))

if __name__ == "__main__":
    main()
