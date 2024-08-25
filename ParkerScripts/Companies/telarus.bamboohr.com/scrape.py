from selenium import webdriver
import os
from dotenv import load_dotenv

load_dotenv()
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
import shutil
import threading
import sys
import json

profile_folder_path = os.getenv("CHROME_PROFILE_PATH") + os.path.sep + str(threading.get_ident())
service = Service(executable_path=r""+os.getenv("CHROME_DRIVER_PATH")+"")
options = webdriver.ChromeOptions()
options.add_argument(f"user-data-dir={profile_folder_path}")
options.add_argument("--headless")
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")

driver = webdriver.Chrome(service=service, options=options)
file_name = sys.argv[1]
driver.get(f"file:///{file_name}")

job_blocks_selector = "ul > div"
job_title_selector = ".fabric-5qovnk-root.MuiBox-root.css-7ebljt"
job_url_selector = "a"

job_elements = driver.find_elements(By.CSS_SELECTOR, job_blocks_selector)
result = []

for job_element in job_elements:
    job_title_element = job_element.find_element(By.CSS_SELECTOR, job_title_selector)
    job_url_element = job_element.find_element(By.CSS_SELECTOR, job_url_selector)
    result.append({"Job-title": job_title_element.text, "URL": job_url_element.get_attribute('href')})

print(json.dumps(result))

driver.quit()
