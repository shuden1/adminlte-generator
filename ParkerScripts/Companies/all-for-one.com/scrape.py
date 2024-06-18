import sys
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
import threading
import json

# Target HTML file name received as a console command argument
target_html_file = sys.argv[1]

# WebDriver profile path setup
profile_folder_path = "D:\\Mind\\CRA\\AI_Experiments\\Job_Crawlers\\Peter\\adminlte-generator\\chrome_profile\\" + str(threading.get_ident())

# WebDriver option and service configuration
options = webdriver.ChromeOptions()
options.add_argument(f"user-data-dir={profile_folder_path}")
options.add_argument("--headless")
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")
service = Service(executable_path=r"C:\Python3\chromedriver.exe")

# Initialize WebDriver
driver = webdriver.Chrome(service=service, options=options)

# Open the target HTML file
driver.get(f"file:///{target_html_file}")

# Extract job listings using identified selectors
job_listings = driver.find_elements(By.CSS_SELECTOR, ".molecule-job-teaser")
job_data = []

# Iterate through job listings to extract job titles and URLs
for job in job_listings:
    title = job.find_element(By.CSS_SELECTOR, ".job-title").text
    url = job.get_attribute("href")
    job_data.append({"Job-title": title, "URL": url})

# Closing the driver
driver.quit()

# Output the extracted job listings as JSON
print(json.dumps(job_data))