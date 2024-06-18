import sys
import json
import threading
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

# Retrieve the HTML file name from the command line arguments
html_file_path = sys.argv[1]

# Selenium setup
profile_folder_path = f"D:\\Mind\\CRA\\AI_Experiments\\Job_Crawlers\\Peter\\adminlte-generator\\chrome_profile\\{threading.get_ident()}"
service = Service(executable_path=r"C:\Python3\chromedriver.exe")
options = Options()
options.add_argument(f"user-data-dir={profile_folder_path}")
options.add_argument("--headless")
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")

# Initialize WebDriver
driver = webdriver.Chrome(service=service, options=options)

# Open the HTML file
driver.get(f"file:///{html_file_path}")

# Collect job information
job_listings = []
for job in driver.find_elements(By.CSS_SELECTOR, "li.career-position a"):
    job_title = job.text
    job_url = job.get_attribute("href")
    # Assuming the job title and URL are correctly found
    if job_title and job_url:
        job_listings.append({"Job-title": job_title, "URL": job_url})

# Convert job listings to JSON format
jobs_json = json.dumps(job_listings, ensure_ascii=False)

print(jobs_json)

# Cleanup
driver.quit()