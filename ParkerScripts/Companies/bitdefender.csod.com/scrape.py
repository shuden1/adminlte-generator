import sys
from selenium import webdriver
import os
from dotenv import load_dotenv

load_dotenv()
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
import threading
import shutil
import json

# Selectors from STEP 1
job_block_selector = '.p-panel.p-bg-white.p-p-md.p-bw-xs.p-bc-grey70.p-bs-solid.rounded-all'
job_title_selector = 'a[data-tag="displayJobTitle"] > p'
job_url_selector = 'a[data-tag="displayJobTitle"]'

def get_job_listings(html_file):
    profile_folder_path = f"D:\\Mind\\CRA\\AI_Experiments\\Job_Crawlers\\Peter\\adminlte-generator\\chrome_profile\\{threading.get_ident()}"
    service = ChromeService(executable_path=r""+os.getenv("CHROME_DRIVER_PATH")+"")
    options = webdriver.ChromeOptions()
    options.add_argument(f"user-data-dir={profile_folder_path}")
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")

    driver = webdriver.Chrome(service=service, options=options)
    driver.get(f"file://{html_file}")

    jobs = []
    job_blocks = driver.find_elements(By.CSS_SELECTOR, job_block_selector)
    for job_block in job_blocks:
        title_element = job_block.find_element(By.CSS_SELECTOR, job_title_selector)
        url_element = job_block.find_element(By.CSS_SELECTOR, job_url_selector)
        jobs.append({"Job-title": title_element.text, "URL": url_element.get_attribute('href')})

    driver.quit()


    return json.dumps(jobs)

# Using the first command line argument as the HTML file name
if __name__ == '__main__':
    file_name = sys.argv[1]
    print(get_job_listings(file_name))
