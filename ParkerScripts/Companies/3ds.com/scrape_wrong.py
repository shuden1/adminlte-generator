import sys
import threading
from selenium import webdriver
import os
from dotenv import load_dotenv

load_dotenv()
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service

# Retrieve the HTML file name from command line argument
html_file_name = sys.argv[1]

# Set up Chrome driver options
options = webdriver.ChromeOptions()
profile_path = os.getenv("CHROME_PROFILE_PATH") + "\\" + str(threading.get_ident())
options.add_argument(f"user-data-dir={profile_path}")
options.add_argument("--headless")
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")

# Initialize Chrome driver
service = Service(executable_path=r""+os.getenv("CHROME_DRIVER_PATH")+"")
driver = webdriver.Chrome(service=service, options=options)

# Open the local HTML file
driver.get(f"file:///{html_file_name}")

# Scraping jobs data
jobs_data = []
# Assuming selectors are correctly replaced based on file content analysis
job_elements = driver.find_elements(By.CSS_SELECTOR, ".job-listing .job-title a")
for job_element in jobstock_elements:
    job_title = job_element.text
    job_url = job_element.get_attribute('href')
    jobs_data.append({"Job-title": job_title, "URL": job_url})

driver.quit()

# Print jobs data as JSON
print(jobs_data)
