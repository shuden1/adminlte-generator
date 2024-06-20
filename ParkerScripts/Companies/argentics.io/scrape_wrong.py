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

    job_listings = []

    # Replace 'YOUR_JOB_BLOCK_SELECTOR' with the actual selector for job blocks
    job_blocks = driver.find_elements(By.CSS_SELECTOR, '[data-job-block]')

    for job_block in job_blocks:
        # Replace 'YOUR_JOB_TITLE_SELECTOR' with the actual selector for job titles
        job_title_element = job_block.find_element(By.CSS_SELECTOR, '[data-job-title]')
        job_title = job_title_element.text
        job_url = job_title_element.get_attribute('href')

        job_listings.append({"Job-title": job_title, "URL": job_url})

    driver.quit()

    return json.dumps(job_listings, indent=4)

if __name__ == "__main__":
    file_path = sys.argv[1]
    print(scrape_jobs(file_path))
