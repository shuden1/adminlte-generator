from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
import threading
import shutil
import sys
import json

# STEP 2
html_file = sys.argv[1]
job_block_class = "jobs-list-item"
job_title_selector = "div.job-title > span"
job_url_selector = "a.au-target"

profile_folder_path = "D:\\Mind\\CRA\\AI_Experiments\\Job_Crawlers\\Peter\\adminlte-generator\\chrome_profile\\" + str(threading.get_ident())
service = Service(executable_path=r"C:\Python3\chromedriver.exe")

options = webdriver.ChromeOptions()
options.add_argument(f"user-data-dir={profile_folder_path}")
options.add_argument("--headless")
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")

driver = webdriver.Chrome(service=service, options=options)
driver.get(f"file://{html_file}")

job_listings = []
job_elements = driver.find_elements(By.CSS_SELECTOR, f'.{job_block_class}')
for job_element in job_elements:
    title_element = job_element.find_element(By.CSS_SELECTOR, job_title_selector)
    url_element = job_element.find_element(By.CSS_SELECTOR, job_url_selector)
    job_title = title_element.text
    job_url = url_element.get_attribute('href')
    job_listings.append({"Job-title": job_title, "URL": job_url})

print(json.dumps(job_listings))

driver.quit()
shutil.rmtree(profile_folder_path)
