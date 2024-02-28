import json
import shutil
import sys
import threading
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By

# Get the HTML file name from the command line argument
html_file_name = sys.argv[1]

# Initialise a headless webdriver
options = webdriver.ChromeOptions()
options.add_argument('--headless')
options.add_argument('--disable-gpu')
profile_folder_path = "D:\\Mind\\CRA\\AI_Experiments\\Job_Crawlers\\Peter\\adminlte-generator\\chrome_profile\\" + str(threading.get_ident())
options.add_argument(f"user-data-dir={profile_folder_path}")
service = ChromeService(executable_path=r"C:\Python3\chromedriver.exe")
driver = webdriver.Chrome(service=service, options=options)

# Open the local HTML file
driver.get(f"file:///{html_file_name}")

# Selectors defined from STEP 1
job_list_selector = '.css-8j5iuw'
job_title_selector = '.css-19uc56f'

# Scrape all job listings
jobs = driver.find_elements(By.CSS_SELECTOR, f"{job_list_selector} {job_title_selector}")
job_listings = []
for job in jobs:
    job_title_text = job.text
    job_url = job.get_attribute('href')
    job_listings.append({"Job-title": job_title_text, "URL": job_url})

# Return a JSON
print(json.dumps(job_listings))

# Close the driver
driver.quit()

# Remove the profile folder
shutil.rmtree(profile_folder_path)