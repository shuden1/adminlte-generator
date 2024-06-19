from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
import json
import sys
import threading

# Step 2: Python + Selenium Script Enhanced Based on Feedback

# Read the HTML file name from the command line argument
html_file_name = sys.argv[1]

# Set up ChromeDriver options and service
profile_folder_path = "D:\\Mind\\CRA\\AI_Experiments\\Job_Crawlers\\Peter\\adminlte-generator\\chrome_profile\\" + str(threading.get_ident())
service = ChromeService(executable_path=r"C:\Python3\chromedriver.exe")
options = webdriver.ChromeOptions()
options.add_argument(f"user-data-dir={profile_folder_path}")
options.add_argument("--headless")
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")

# Initialize WebDriver
driver = webdriver.Chrome(service=service, options=options)

# Open the local HTML file
driver.get(f"file:///{html_file_name}")

# Use corrected selectors to find job listings
# Enhancement: Explicitly targeting links with non-empty titles and valid URLs
jobs = driver.find_elements(By.CSS_SELECTOR, ".MuiDataGrid-row--dynamicHeight a[href]:not([href*='locations']):not(:empty) > h6.MuiTypography-subtitle1")
jobs_data = []

for job in jobs:
    job_title = job.text.strip()
    job_url = job.find_element(By.XPATH, "..").get_attribute('href').strip()
    if job_title and job_url:
        jobs_data.append({"Job-title": job_title, "URL": job_url})

# Output the result as JSON without closing driver for quick adjustments or further navigation if necessary
print(json.dumps(jobs_data, indent=4))