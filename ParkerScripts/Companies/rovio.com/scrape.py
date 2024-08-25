import sys
from selenium import webdriver
import os
from dotenv import load_dotenv

load_dotenv()
from selenium.webdriver.chrome.service import Service as service
from selenium.webdriver.common.by import By
import json
import threading

# Step 2: Parse the command line argument for HTML file name
target_html_file_name = sys.argv[1]

# Step 3: Webdriver initialization
profile_folder_path = os.getenv("CHROME_PROFILE_PATH") + "\\" + str(threading.get_ident())
options = webdriver.ChromeOptions()
options.add_argument(f"user-data-dir={profile_folder_path}")
options.add_argument("--headless")
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")
driver_service = service(executable_path=r""+os.getenv("CHROME_DRIVER_PATH")+"")
driver = webdriver.Chrome(service=driver_service, options=options)

# Step 4: Scrape the job listings
driver.get(f'file:///{target_html_file_name}')
job_elements = driver.find_elements(By.CSS_SELECTOR, ".c-open-po-card__title")
jobs = []

for job_title_element in job_elements:
    job_title = job_title_element.get_attribute("innerText")
    job_url = job_title_element.get_attribute("href")
    jobs.append({"Job-title": job_title, "URL": job_url})

# Step 5: Close the driver and return the scraped data as JSON
driver.quit()
print(json.dumps(jobs))
