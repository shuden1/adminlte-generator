import sys
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
import json
import threading

# Retrieve the HTML file name from the command line arguments
target_html_file = sys.argv[1]

# Initialising a headless webdriver
options = webdriver.ChromeOptions()
profile_folder_path = f"D:\\Mind\\CRA\\AI_Experiments\\Job_Crawlers\\Peter\\adminlte-generator\\chrome_profile\\{str(threading.get_ident())}"
options.add_argument(f"user-data-dir={profile_folder_path}")
options.add_argument("--headless")
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")
service = ChromeService(executable_path=r"C:\Python3\chromedriver.exe")

driver = webdriver.Chrome(service=service, options=options)

# Opening the target HTML file
driver.get(f"file:///{target_html_file}")

# Scraping job listings using the selectors defined from the uploaded HTML document
job_listings = driver.find_elements(By.CSS_SELECTOR, ".vacancy-item")

jobs = []
for job in job_listings:
    title = job.find_element(By.CSS_SELECTOR, ".vacancy-item__title").text
    url = job.get_attribute("href")
    jobs.append({"Job-title": title, "URL": url})

# Converting the job list to JSON
jobs_json = json.dumps(jobs)

# Closing the driver
driver.quit()

# Outputting the job list in JSON format
print(jobs_json)