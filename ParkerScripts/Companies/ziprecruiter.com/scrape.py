from selenium import webdriver
import os
from dotenv import load_dotenv

load_dotenv()
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
import json
import shutil
import sys
import threading

# The target HTML file name should be an argument sent from an external source through the console command as the single input parameter.
html_file_path = sys.argv[1]  # sys.argv[0] is the script name

# Initialise a headless webdriver
options = webdriver.ChromeOptions()
profile_folder_path = os.getenv("CHROME_PROFILE_PATH") + "\\" + str(threading.get_ident())
options.add_argument("user-data-dir=" + profile_folder_path)
options.add_argument("--headless")
service = ChromeService(executable_path=r""+os.getenv("CHROME_DRIVER_PATH")+"")
driver = webdriver.Chrome(service=service, options=options)

# Scrape all job listings using the selectors defined in STEP 1
driver.get("file:///" + html_file_path)
job_elements = driver.find_elements(By.CSS_SELECTOR, "a.job_title")
jobs = [{"Job-title": el.text, "URL": el.get_attribute("href")} for el in job_elements]

# Return a JSON in the following format
print(json.dumps(jobs))

# Remove the folder profile_folder_path
driver.quit()
