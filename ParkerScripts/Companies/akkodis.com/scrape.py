import sys
from selenium import webdriver
import os
from dotenv import load_dotenv

load_dotenv()
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
import json
import threading

# Retrieve the target HTML file name from the external source (console command)
target_html_file_name = sys.argv[1]

# Initialize a headless webdriver
profile_folder_path = os.getenv("CHROME_PROFILE_PATH") + os.path.sep + str(threading.get_ident())
service = ChromeService(executable_path=r""+os.getenv("CHROME_DRIVER_PATH")+"")
options = webdriver.ChromeOptions()
options.add_argument(f"user-data-dir={profile_folder_path}")
options.add_argument("--headless")
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")

driver = webdriver.Chrome(service=service, options=options)

# Open the target HTML file
driver.get(f"file:///{target_html_file_name}")

# Scrape all job listings
job_links = driver.find_elements(By.CSS_SELECTOR, "li > a[href]")
jobs_list = []

for job_link in job_links:
    try:
        job_title = job_link.find_element(By.CSS_SELECTOR, "h3").text
        job_url = job_link.get_attribute('href')
        if job_title and job_url:
            jobs_list.append({"Job-title": job_title, "URL": job_url})
    except:
        continue

# Return a JSON
print(json.dumps(jobs_list))

# Done with the driver
driver.quit()
