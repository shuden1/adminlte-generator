import sys
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
import shutil
import threading
import json

# STEP 1
job_openings_selector = '.iCIMS_JobSearchTable'
job_title_and_url_selector = 'a.iCIMS_Anchor'

# The target HTML file name should be an input argument.
target_html_file = sys.argv[1]

# STEP 2
profile_folder_path = "D:\\Mind\\CRA\\AI_Experiments\\Job_Crawlers\\Peter\\adminlte-generator\\chrome_profile\\" + str(threading.get_ident())
options = webdriver.ChromeOptions()
options.add_argument(f"user-data-dir={profile_folder_path}")
options.headless = True
service = ChromeService(executable_path=r"C:\Python3\chromedriver.exe")
driver = webdriver.Chrome(service=service, options=options)

# Load the HTML page from the file system.
driver.get(f"file://{target_html_file}")

# Scrape all job listings using the selectors from STEP 1.
job_listings = driver.find_elements(By.CSS_SELECTOR, job_openings_selector)
jobs = []

for job_listing in job_listings:
    titles_and_urls = job_listing.find_elements(By.CSS_SELECTOR, job_title_and_url_selector)
    for title_and_url in titles_and_urls:
        jobs.append({"Job-title": title_and_url.text, "URL": title_and_url.get_attribute('href')})

# Convert the list of jobs to JSON.
json_output = json.dumps(jobs)

# Close the driver and remove the profile folder.
driver.quit()
shutil.rmtree(profile_folder_path)

# Return the JSON output.
print(json_output)