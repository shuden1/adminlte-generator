from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
import threading
import sys
import json

# Retrieve the target file name from the argument passed via console command
target_file_name = sys.argv[1]

# Job opening block selector
job_openings_block_selector = ".styles--3Cb9F"

# Job title and URL selector
job_title_selector = "h3"
job_title_container_selector = "a"

# Set up webdriver service
service = ChromeService(executable_path=r"C:\Python3\chromedriver.exe")

# Set up options for the webdriver
options = webdriver.ChromeOptions()
profile_folder_path = "D:\\Mind\\CRA\\AI_Experiments\\Job_Crawlers\\Peter\\adminlte-generator\\chrome_profile\\" + str(threading.get_ident())
options.add_argument(f"user-data-dir={profile_folder_path}")
options.add_argument("--headless")
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")

# Initialise a headless webdriver
driver = webdriver.Chrome(service=service, options=options)
driver.get(f"file:///{target_file_name}")

# Scrape all job listings using the defined selectors from STEP 1
job_listings = []
job_blocks = driver.find_elements(By.CSS_SELECTOR, job_openings_block_selector)
for block in job_blocks:
    job_title_element = block.find_element(By.CSS_SELECTOR, job_title_selector)
    job_title = job_title_element.text
    link_element = block.find_element(By.CSS_SELECTOR, job_title_container_selector)
    job_url = link_element.get_attribute("href")
    job_listings.append({"Job-title": job_title, "URL": job_url})

driver.quit()

# Return a JSON of the job listings
print(json.dumps(job_listings))