from selenium import webdriver
import os
from dotenv import load_dotenv

load_dotenv()
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
import json, sys, threading

file_name = sys.argv[1]

service = ChromeService(executable_path=r""+os.getenv("CHROME_DRIVER_PATH")+"")
options = webdriver.ChromeOptions()
profile_folder_path = os.getenv("CHROME_PROFILE_PATH") + "\\" + str(threading.get_ident())
options.add_argument(f"user-data-dir={profile_folder_path}")
options.add_argument("--headless")
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")

driver = webdriver.Chrome(service=service, options=options)
driver.get(f"file:///{file_name}")

job_blocks_selector = ".c-jobs-list-wrap.jobs-list-only ul.results-list.front > li.results-list__item"
job_titles_selector = ".results-list__item-title"
job_urls_selector = ".results-list__item-title"

job_listings = []
for job_block in driver.find_elements(By.CSS_SELECTOR, job_blocks_selector):
    job_title_element = job_block.find_element(By.CSS_SELECTOR, job_titles_selector)
    job_title = job_title_element.text
    job_url = job_title_element.get_attribute('href')
    job_listings.append({"Job-title": job_title, "URL": job_url})

print(json.dumps(job_listings))
driver.quit()
