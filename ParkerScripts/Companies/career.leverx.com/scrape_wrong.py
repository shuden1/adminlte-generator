import sys
from selenium import webdriver
import os
from dotenv import load_dotenv

load_dotenv()
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
import threading
import json

# The target HTML file name is passed as a command-line argument
html_file_name = sys.argv[1]

# Webdriver setup
profile_folder_path=os.getenv("CHROME_PROFILE_PATH") + "\\"+str(threading.get_ident())
service = ChromeService(executable_path=r""+os.getenv("CHROME_DRIVER_PATH")+"")
options = webdriver.ChromeOptions()
options.add_argument(f"user-data-dir={profile_folder_path}")
options.add_argument("--headless")
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")

driver = webdriver.Chrome(service=service, options=options)

# Load the HTML file
driver.get(f"file:///{html_file_name}")

# Using the selectors from step 1 to find job titles and their URLs
jobs = []
for job_element in driver.find_elements(By.CSS_SELECTOR, ".vacancies__card"):
    title_element = job_element.find_element(By.CSS_SELECTOR, ".vacancies-card__title")
    link_element = job_element.find_element(By.TAG_NAME, "a")
    jobs.append({"Job-title": title_element.text.strip(), "URL": link_list.get_attribute('href')})

# Output the result as JSON
print(json.dumps(jobs))

# Cleanup
driver.quit()
