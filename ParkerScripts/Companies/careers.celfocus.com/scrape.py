import sys
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
import threading
import json

# Accepting target HTML file name from console command
target_html_file = sys.argv[1]

# Webdriver setup
profile_folder_path = "D:\\Mind\\CRA\\AI_Experiments\\Job_Crawlers\\Peter\\adminlte-generator\\chrome_profile\\" + str(threading.get_ident())
service = Service(executable_path=r"C:\Python3\chromedriver.exe")
options = webdriver.ChromeOptions()
options.add_argument(f"user-data-dir={profile_folder_path}")
options.add_argument("--headless")
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")

# Start headless browser session
driver = webdriver.Chrome(service=service, options=options)

# Open the target HTML file
driver.get(f"file:///{target_html_file}")

# Selectors identified in Step 1
job_block_selector = ".block-grid-item"
job_title_selector = ".text-block-base-link"
job_url_selector = "a"

# Scraping job listings
job_elements = driver.find_elements(By.CSS_SELECTOR, job_block_selector)
jobs = []

for job_element in job_elements:
    title_element = job_element.find_element(By.CSS_SELECTOR, job_title_selector)
    url_element = job_element.find_element(By.CSS_SELECTOR, job_url_selector)
    jobs.append({"Job-title": title_element.get_attribute('title'), "URL": url_element.get_attribute('href')})

# Output result
print(json.dumps(jobs))

# Close browser session
driver.quit()