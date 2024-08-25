import sys
from selenium import webdriver
import os
from dotenv import load_dotenv

load_dotenv()
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
import threading
import json

# Read target HTML file name from command line argument
target_html_file = sys.argv[1]

# Webdriver setup
profile_folder_path = os.getenv("CHROME_PROFILE_PATH") + "\\"+str(threading.get_ident())
service = ChromeService(executable_path=r""+os.getenv("CHROME_DRIVER_PATH")+"")
options = webdriver.ChromeOptions()
options.add_argument(f"user-data-dir={profile_folder_path}")
options.add_argument("--headless")
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")

driver = webdriver.Chrome(service=service, options=options)

# Open the local HTML file
url = f"file:///{target_html_file}"
driver.get(url)

# Selector & data collection
job_elements = driver.find_elements(By.CSS_SELECTOR, ".career-list__item")

jobs = []
for job_element in job_elements:
    title = job_element.find_element(By.CSS_SELECTOR, ".career-list__headline").text
    url = job_element.find_element(By.CSS_SELECTOR, ".career-list__button.full-width").get_attribute('href')
    jobs.append({"Job-title": title, "URL": url})

# Close the driver
driver.quit()

# Output
print(json.dumps(jobs))
