import sys
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
import shutil
import threading
import json

# The target HTML file name is an argument sent from an external source through the console command as the single input parameter.
target_html_filename = sys.argv[1]

# Initialize a headless webdriver with a profile path.
profile_folder_path = "D:\\Mind\\CRA\\AI_Experiments\\Job_Crawlers\\Peter\\adminlte-generator\\chrome_profile\\" + str(threading.get_ident())
options = webdriver.ChromeOptions()
options.add_argument(f"user-data-dir={profile_folder_path}")
options.add_argument("--headless")
service = ChromeService(executable_path=r"C:\Python3\chromedriver.exe")

# Start the browser with the configured options
driver = webdriver.Chrome(service=service, options=options)

# Open the local HTML file
driver.get(f"file:///{target_html_filename}")

# Define the BeautifulSoup selectors identified in Step 1 for Job Openings and select job titles and associated URLs
job_opening_block_selector = ".department"
job_title_selector = ".name"
job_url_selector = "a.job"

# Scrape all job listings using the above selectors
job_elements = driver.find_elements(By.CSS_SELECTOR, f"{job_opening_block_selector} {job_url_selector}")
jobs = [{"Job-title": job_el.find_element(By.CSS_SELECTOR, job_title_selector).text, 
         "URL": job_el.get_attribute('href')} for job_el in job_elements]

# Cast the list of dictionaries to JSON format
jobs_json = json.dumps(jobs)

print(jobs_json)

# Clean up: Close the browser and remove the user profile folder
driver.quit()
shutil.rmtree(profile_folder_path)