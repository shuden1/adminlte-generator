import sys
from selenium import webdriver
import os
from dotenv import load_dotenv

load_dotenv()
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
import json
import threading

# Parsing argument for HTML file name
file_name = sys.argv[1]

# Initialize a headless ChromeDriver
service = ChromeService(executable_path=r""+os.getenv("CHROME_DRIVER_PATH")+"")
profile_folder_path = os.getenv("CHROME_PROFILE_PATH") + "\\" + str(threading.get_ident())
options = webdriver.ChromeOptions()
options.add_argument(f"user-data-dir={profile_folder_path}")
options.add_argument("--headless")
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")

driver = webdriver.Chrome(service=service, options=options)

# Preparing the URL by assuming the HTML file is accessible via a local file URL
url = f"file:///{file_name}"
driver.get(url)

# Fetch job postings
job_postings = []
job_elements = driver.find_elements(By.CSS_SELECTOR, ".jobs-container ul li a")

for job_element in job_elements:
    job_title = job_element.find_element(By.CSS_SELECTOR, "span.text-block-base-link").get_attribute("title")
    job_url = job_element.get_attribute("href")
    job_postings.append({"Job-title": job_title, "URL": job_url})

print(json.dumps(job_postings, indent=2))
driver.quit()
