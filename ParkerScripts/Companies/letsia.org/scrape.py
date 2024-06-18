from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
import json
import sys
import threading

# The target HTML file name received from the console command as the input parameter
html_file_name = sys.argv[1]

# Initialising a headless webdriver
service = ChromeService(executable_path=r"C:\Python3\chromedriver.exe")
options = webdriver.ChromeOptions()
profile_folder_path = "D:\\Mind\\CRA\\AI_Experiments\\Job_Crawlers\\Peter\\adminlte-generator\\chrome_profile\\" + str(threading.get_ident())
options.add_argument(f"user-data-dir={profile_folder_path}")
options.add_argument("--headless")
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")

driver = webdriver.Chrome(service=service, options=options)

# Open the provided HTML file 
driver.get(f"file:///{html_file_name}")

# Define the exact selectors
job_blocks_selector = ".job-section .table-responsive table tbody tr"
job_title_selector = "td:first-child"
job_url_selector = "td a"  # Assuming there is an <a> tag within the TD for URLs

jobs = []

for job_block in driver.find_elements(By.CSS_SELECTOR, job_blocks_selector):
    job_title = job_block.find_element(By.CSS_SELECTOR, job_title_selector).text
    try:
        job_url = job_block.find_element(By.CSS_SELECTOR, job_url_selector).get_attribute('href')
    except:
        job_url = ""
    jobs.append({"Job-title": job_title, "URL": job_url})

driver.quit()

# Output the scraped data as JSON
print(json.dumps(jobs))