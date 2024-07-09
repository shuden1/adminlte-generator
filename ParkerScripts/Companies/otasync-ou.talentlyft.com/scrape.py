import sys
import json
import threading
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

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

    job_blocks_selector = '.jobs__body'  # Use the correct selector identified in STEP 1
    job_title_selector = 'a .jobs__box__heading'  # Use the correct selector identified in STEP 1
    job_url_selector = 'a'  # Use the correct selector identified in STEP 1

    job_blocks = driver.find_elements(By.CSS_SELECTOR, job_blocks_selector)

    jobs = []
    for job_block in job_blocks:
        title_element = job_block.find_element(By.CSS_SELECTOR, job_title_selector)
        job_title = title_element.text.strip()

        url_element = job_block.find_element(By.CSS_SELECTOR, job_url_selector)
        job_url = url_element.get_attribute('href')
        jobs.append({"Job-title": job_title, "URL": job_url})

    driver.quit()

    return json.dumps(jobs, indent=4)

if __name__ == "__main__":
    file_path = sys.argv[1]
    print(scrape_jobs(file_path))
