import json
import shutil
import sys
import threading
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService

# The target HTML file name is obtained from the argument sent from the external source through the console command
html_file_name = sys.argv[1]

# Set up a profile folder path for the headless webdriver
profile_folder_path = "D:\\Mind\\CRA\\AI_Experiments\\Job_Crawlers\\Peter\\adminlte-generator\\chrome_profile\\" + str(threading.get_ident())

# Configure ChromeDriver
service = ChromeService(executable_path=r"C:\Python3\chromedriver.exe")
options = webdriver.ChromeOptions()
options.add_argument(f"user-data-dir={profile_folder_path}")
options.add_argument("--headless")
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")

# Initialize the driver
driver = webdriver.Chrome(service=service, options=options)

# Open the HTML file
driver.get(f'file:///{html_file_name}')

# Selectors as identified in STEP 1
job_blocks_selector = '.js-section-job-list .js-job-departament-container'
job_title_selector = '.js-job-title a'

# Scrape the data
job_listings = driver.find_elements(By.CSS_SELECTOR, job_blocks_selector)
jobs_data = []

for job_block in job_listings:
    job_titles = job_block.find_elements(By.CSS_SELECTOR, job_title_selector)
    for job_title in job_titles:
        job_data = {
            "Job-title": job_title.text,
            "URL": job_title.get_attribute('href')
        }
        jobs_data.append(job_data)

# Close the driver
driver.quit()

# Remove the profile folder


# Output the result as JSON
print(json.dumps(jobs_data))
