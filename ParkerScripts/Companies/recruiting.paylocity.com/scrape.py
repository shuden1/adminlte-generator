import sys
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
import threading
import shutil
import json

# STEP 1:
# Selectors for job openings block
job_openings_block_selector = ".job-listing-container"
# Selectors for job titles and URLs
job_title_selector = ".job-item-title a"

# STEP 2:
# External input for the filename
html_file_path = sys.argv[1]

# Initialize headless webdriver
profile_folder_path = f"D:\\Mind\\CRA\\AI_Experiments\\Job_Crawlers\\Peter\\adminlte-generator\\chrome_profile\\{str(threading.get_ident())}"
service = ChromeService(executable_path=r"C:\Python3\chromedriver.exe")
options = webdriver.ChromeOptions()
options.add_argument(f"user-data-dir={profile_folder_path}")
options.add_argument("--headless")
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")

driver = webdriver.Chrome(service=service, options=options)

# Open the local HTML file
driver.get(f"file://{html_file_path}")

# Scrape job listings
job_listings = []
job_elements = driver.find_elements(By.CSS_SELECTOR, f"{job_openings_block_selector} {job_title_selector}")
for job_element in job_elements:
    job_title = job_element.text
    job_url = job_element.get_attribute('href')
    job_listings.append({"Job-title": job_title, "URL": job_url})

# Output the job listings in JSON format
print(json.dumps(job_listings))

# Close the driver and remove the profile folder
driver.quit()
