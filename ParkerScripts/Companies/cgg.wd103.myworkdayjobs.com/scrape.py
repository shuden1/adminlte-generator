from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import json
import sys
import threading

# Getting the HTML file name from the command line argument
html_file_name = sys.argv[1]

# Setup for ChromeDriver with specified options and service
profile_folder_path = "D:\\Mind\\CRA\\AI_Experiments\\Job_Crawlers\\Peter\\adminlte-generator\\chrome_profile\\" + str(threading.get_ident())

options = webdriver.ChromeOptions()
options.add_argument(f"user-data-dir={profile_folder_path}")
options.add_argument("--headless")
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")

service = Service(executable_path=r"C:\Python3\chromedriver.exe")

# Initialize ChromeDriver
driver = webdriver.Chrome(service=service, options=options)

# Load the HTML file
driver.get(f"file:///{html_file_name}")

# Selectors defined in Step 1 (Example placeholders to be replaced with actual selectors obtained in Step 1)
job_block_selector = '.css-1q2dra3'  # Job listing block selector
job_title_selector = 'h3 a.css-19uc56f'  # Job title selector within block

# Scraping job listings
job_listings = []
for job in driver.find_elements(By.CSS_SELECTOR, job_block_selector):
    job_title = job.find_element(By.CSS_SELECTOR, job_title_selector).text
    job_url = job.find_element(By.CSS_SELECTOR, job_title_selector).get_attribute('href')
    job_listings.append({"Job-title": job_title, "URL": job_url})

driver.quit()

# Converting the jobs list to JSON format
json_output = json.dumps(job_listings)
print(json_output)