import sys
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import threading
import json

# The target HTML file name should come from the command line argument
html_file_path = sys.argv[1]

# Setting up the service and options for ChromeDriver
profile_folder_path = "D:\\Mind\\CRA\\AI_Experiments\\Job_Crawlers\\Peter\\adminlte-generator\\chrome_profile\\" + str(threading.get_ident())
service = Service(executable_path=r"C:\Python3\chromedriver.exe")
options = webdriver.ChromeOptions()
options.add_argument(f"user-data-dir={profile_folder_path}")
options.add_argument("--headless")
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")

# Start the headless webdriver
driver = webdriver.Chrome(service=service, options=options)

# Open the HTML file
driver.get(f"file:///{html_file_path}")

# Scrape all job listings using the selectors identified in STEP 1
job_listings = []
for job_block in driver.find_elements(By.CSS_SELECTOR, ".JobBlockcss__ContainerWrapper-sc-6e8iiq-0"):
    job_title = job_block.find_element(By.CSS_SELECTOR, ".job-title").text
    job_link = job_block.find_element(By.CSS_SELECTOR, "a").get_attribute("href")
    job_listings.append({"Job-title": job_title, "URL": job_link})

# Output the scraped job listings in JSON format
print(json.dumps(job_listings))

driver.quit()