import sys
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
import json
import threading

# The target HTML file name is taken from the console command argument
target_html_file = sys.argv[1]

# Initialise a headless webdriver
profile_folder_path = f"D:\\Mind\\CRA\\AI_Experiments\\Job_Crawlers\\Peter\\adminlte-generator\\chrome_profile\\{threading.get_ident()}"
service = ChromeService(executable_path=r"C:\Python3\chromedriver.exe")
options = webdriver.ChromeOptions()
options.add_argument(f"user-data-dir={profile_folder_path}")
options.add_argument("--headless")
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")

driver = webdriver.Chrome(service=service, options=options)

# Open the target HTML file
driver.get(f"file:///{target_html_file}")

# Scrape all job listings. Adjusting selector placeholders for demonstration purposes
# Example correct selectors based on common structures, to be adjusted for real use case
job_listings = []
for job_element in driver.find_elements(By.CSS_SELECTOR, ".job-listing"):
    job_title = job_element.find_element(By.CSS_SELECTOR, ".job-title").text
    job_url = job_element.find_element(By.CSS_SELECTOR, "a").get_attribute("href")
    job_listings.append({"Job-title": job_title, "URL": job_url})

# Return a JSON format of job listings
print(json.dumps(job_listings))

driver.quit()