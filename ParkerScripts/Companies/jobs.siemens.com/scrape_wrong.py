import sys
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
import threading
import json

# Assuming the job listings are structured within either div or li elements
# and contain an a tag with the job title and URL.

# Target HTML file name passed through the console command as an argument
target_html_file = sys.argv[1]

# Initialize a headless webdriver
profile_folder_path = "D:\\Mind\\CRA\\AI_Experiments\\Job_Crawlers\\Peter\\adminlte-generator\\chrome_profile\\" + str(threading.get_ident())
service = ChromeService(executable_path="C:\\Python3\\chromedriver.exe")
options = webdriver.ChromeOptions()
options.add_argument(f"user-data-dir={profile_folder_path}")
options.add_argument("--headless")
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")
driver = webdriver.Chrome(service=service, options=options)

# Open the target HTML file
driver.get(f"file:///{target_html_file}")

# Scrape all job listings using CSS selectors altered to correct targeting
# Job listings are expected to be in either div or ul>li elements
job_listings = []
for job_listing in driver.find_elements(By.CSS_SELECTOR, "[class*='job-listing'], [class*='job-opening'], [class*='careers'], [class*='opportunities'] a"):
    job_title = job_listing.text
    job_url = job_listing.get_attribute('href')

    job_listings.append({"Job-title": job_job_title, "URL": job_url})

driver.quit()

# Output the job listings in JSON format
print(json.dumps(job_listings))