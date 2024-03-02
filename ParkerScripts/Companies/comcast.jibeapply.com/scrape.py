import sys
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import json
import threading

# The target HTML file name is an argument sent from an external source through the console command
html_file_path = sys.argv[1]

# Initialise a headless webdriver
profile_folder_path = "D:\\Mind\\CRA\\AI_Experiments\\Job_Crawlers\\Peter\\adminlte-generator\\chrome_profile\\" + str(threading.get_ident())
service = ChromeService(executable_path=r"C:\Python3\chromedriver.exe")
options = Options()
options.add_argument(f"user-data-dir={profile_folder_path}")
options.add_argument("--headless")
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")

driver = webdriver.Chrome(service=service, options=options)

# Open the HTML file
driver.get(f"file:///{html_file_path}")

# Job listing selectors from STEP 1
job_block_selector = '.mat-expansion-panel.search-result-item'
job_title_selector = '.job-title .job-title-link'

# Scrape all job listings
job_elements = driver.find_elements(By.CSS_SELECTOR, job_block_selector)
job_listings = []

for job_element in job_elements:
    title_element = job_element.find_element(By.CSS_SELECTOR, job_title_selector)
    job_title = title_element.text
    job_url = title_element.get_attribute('href')
    job_listings.append({"Job-title": job_title, "URL": job_url})

driver.quit()

# Return a JSON
print(json.dumps(job_listings))