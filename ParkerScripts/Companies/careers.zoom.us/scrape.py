import json
import shutil
import sys
import time
import threading
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService

# Getting the target HTML filename from the command line argument
target_html_filename = sys.argv[1]

# Initialise a headless webdriver
profile_folder_path = "D:\\Mind\\CRA\\AI_Experiments\\Job_Crawlers\\Peter\\adminlte-generator\\chrome_profile\\" + str(threading.get_ident())
service = ChromeService(executable_path=r"C:\Python3\chromedriver.exe")
options = webdriver.ChromeOptions()
options.add_argument(f"user-data-dir={profile_folder_path}")
options.add_argument("--headless")
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")
driver = webdriver.Chrome(service=service, options=options)

# Open the local HTML file
driver.get(f"file:///{target_html_filename}")

# Use the selectors defined in STEP 1 to scrape all job listings
job_listings = []
jobs = driver.find_elements(By.CSS_SELECTOR, ".card.job-search-results-card")
for job in jobs:
    title_element = job.find_element(By.CSS_SELECTOR, "h3.card-title.job-search-results-card-title a")
    title = driver.execute_script("return arguments[0].innerText;", title_element).strip()
    url = title_element.get_attribute('href').strip()
    if title and url:  # Check if title and the URL are not empty
        job_listings.append({"Job-title": title, "URL": url})
# Return a JSON object
json_output = json.dumps(job_listings)

# Close the webdriver and remove the profile folder
driver.quit()
time.sleep(5)


print(json_output)
