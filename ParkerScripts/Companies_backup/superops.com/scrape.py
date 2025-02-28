import sys
import json
import threading
import shutil
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By

# Take the target HTML file as an argument from the console command
target_html_file = sys.argv[1]

# Initialize a headless webdriver with a profile path
profile_folder_path = "D:\\Mind\\CRA\\AI_Experiments\\Job_Crawlers\\Peter\\adminlte-generator\\chrome_profile\\" + str(threading.get_ident())
options = webdriver.ChromeOptions()
options.add_argument(f"user-data-dir={profile_folder_path}")
options.add_argument('--headless')
options.add_argument('--no-sandbox')
service = ChromeService(executable_path=r"C:\Python3\chromedriver.exe")

# Start the Chrome Driver
driver = webdriver.Chrome(service=service, options=options)

# Open the target HTML file
driver.get(f"file://{target_html_file}")

# Scrape job listings using the updated selectors
job_listings = []
for job_block in driver.find_elements(By.CSS_SELECTOR, "section.jobs a.no-deco"):
    job_title = job_block.find_element(By.CSS_SELECTOR, "h6").text.strip()
    job_url = job_block.get_attribute("href").strip()
    job_listings.append({"Job-title": job_title, "URL": job_url})

# Close the driver
driver.quit()

# Remove the profile folder
shutil.rmtree(profile_folder_path)

# Output the result as JSON
print(json.dumps(job_listings))