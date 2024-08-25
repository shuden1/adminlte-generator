import sys
import threading
from selenium import webdriver
import os
from dotenv import load_dotenv

load_dotenv()
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service

# Extract the html file name from command line arguments
html_file_name = sys.argv[1]

# Selenium WebDriver setup
profile_folder_path = os.getenv("CHROME_PROFILE_PATH") + os.path.sep + str(threading.get_ident())
service = Service(executable_path=r""+os.getenv("CHROME_DRIVER_PATH")+"")
options = webdriver.ChromeOptions()
options.add_argument(f"user-data-dir={profile_folder_path}")
options.add_argument("--headless")
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")

# Initialize Chrome WebDriver
driver = webdriver.Chrome(service=service, options=options)

# Open the HTML file
driver.get(f"file:///{html_file_name}")

# Job listings logic (Placeholder selectors to be replaced with actual ones)
job_listings = driver.find_elements(By.CSS_SELECTOR, "REPLACE_WITH_ACTUAL_SELECTOR_FOR_JOB_BLOCK")
jobs_output = []

for job in job_listings:
    job_title = job.find_element(By.CSS_SELECTOR, "REPLACE_WITH_ACTUAL_SELECTOR_FOR_JOB_TITLE").text
    job_url = job.find_element(By.CSS_SELECTOR, "REPLACE_WITH_ACTUAL_SELECTOR_FOR_JOB_URL").get_attribute('href')
    jobs_output.append({"Job-title": job_title, "URL": job_url})

driver.quit()

# Output the result
print(jobs_output)
