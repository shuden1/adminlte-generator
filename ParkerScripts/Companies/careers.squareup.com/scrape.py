from selenium import webdriver
import os
from dotenv import load_dotenv

load_dotenv()
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
import shutil
import threading
import sys
import json

# Read the target HTML file name from console command
html_file_name = sys.argv[1]

# Selectors based on updated BeautifulSoup analysis
job_block_selector = 'div[data-job-title]'
job_title_attribute = 'data-job-title'
job_url_tag = 'a'
job_url_attribute = 'href'

def scrape_jobs(html_file_name):
    profile_folder_path = os.getenv("CHROME_PROFILE_PATH") + "\\" + str(threading.get_ident())
    options = webdriver.ChromeOptions()
    options.add_argument(f"user-data-dir={profile_folder_path}")
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    service = ChromeService(executable_path=r""+os.getenv("CHROME_DRIVER_PATH")+"")
    driver = webdriver.Chrome(options=options, service=service)

    driver.get(f"file://{html_file_name}")

    jobs_list = []
    job_elements = driver.find_elements(By.CSS_SELECTOR, job_block_selector)
    for job_element in job_elements:
        job_title = job_element.get_attribute(job_title_attribute)
        job_url_element = job_element.find_element(By.TAG_NAME, job_url_tag)
        job_url = job_url_element.get_attribute(job_url_attribute)
        jobs_list.append({"Job-title": job_title, "URL": job_url})

    driver.quit()


    return json.dumps(jobs_list)

print(scrape_jobs(html_file_name))
