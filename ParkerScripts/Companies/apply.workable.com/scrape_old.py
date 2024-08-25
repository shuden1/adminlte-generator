from selenium import webdriver
import os
from dotenv import load_dotenv

load_dotenv()
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
import threading
import sys
import json

html_file = sys.argv[1]

service = ChromeService(executable_path=r""+os.getenv("CHROME_DRIVER_PATH")+"")
options = webdriver.ChromeOptions()
profile_folder_path = os.getenv("CHROME_PROFILE_PATH") + os.path.sep + str(threading.get_ident())
options.add_argument(f"user-data-dir={profile_folder_path}")
options.add_argument("--headless")
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")

driver = webdriver.Chrome(service=service, options=options)
driver.get(f"file:///{html_file}")

job_blocks = driver.find_elements(By.CSS_SELECTOR, "li.styles--3Cb9F")
job_listings = []

for job_block in job_blocks:
    title_element = job_block.find_element(By.CSS_SELECTOR, "h3.styles--1cN5S")
    title = title_element.text
    url = job_block.find_element(By.XPATH, ".//a").get_attribute("href")
    job_listings.append({"Job-title": title, "URL": url})

print(json.dumps(job_listings))
driver.quit()
