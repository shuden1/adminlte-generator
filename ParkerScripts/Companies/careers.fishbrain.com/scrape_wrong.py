import sys
import json
import threading
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

def scrape_jobs(file_path):
    profile_folder_path = "D:\\Mind\\CRA\\AI_Experiments\\Job_Crawlers\\Peter\\adminlte-generator\\chrome_profile\\" + str(threading.get_ident())
    service = Service(executable_path=r"C:\Python3\chromedriver.exe")

    options = Options()
    options.add_argument(f"user-data-dir={profile_folder_path}")
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")

    driver = webdriver.Chrome(service=service, options=options)

    try:
        driver.get(f"file:///{file_path}")

        job_opening_selector = 'YOUR_JOB_OPENING_SELECTOR'
        job_title_selector = 'YOUR_JOB_TITLE_SELECTOR'
        job_url_selector = 'YOUR_JOB_URL_SELECTOR'

        job_elements = driver.find_elements(By.CSS_SELECTOR, job_opening_selector)
        jobs = []

        for job in job_elements:
            title_element = job.find_element(By.CSS_SELECTOR, job_title_selector)
            url_element = job.find_element(By.CSS_SELECTOR, job_url_selector)

            title = title_element.text
            url = url_element.get_attribute('href')

            jobs.append({"Job-title": title, "URL": url})

        print(json.dumps(jobs, indent=4))

    finally:
        driver.quit()

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script.py <path_to_html_file>")
        sys.exit(1)

    file_path = sys.argv[1]
    scrape_jobs(file_path)
