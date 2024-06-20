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

    driver.get(f"file:///{file_path}")

    job_opening_selector = 'a.block.p-8.bg-mint'
    job_title_selector = 'h2.font-bold'
    job_url_attribute = 'href'

    job_elements = driver.find_elements(By.CSS_SELECTOR, job_opening_selector)

    jobs = []
    for job_element in job_elements:
        job_title = job_element.find_element(By.CSS_SELECTOR, job_title_selector).text
        job_url = job_element.get_attribute(job_url_attribute)
        jobs.append({"Job-title": job_title, "URL": job_url})

    driver.quit()

    print(json.dumps(jobs, indent=4))

if __name__ == "__main__":
    file_path = sys.argv[1]
    scrape_jobs(file_path)
