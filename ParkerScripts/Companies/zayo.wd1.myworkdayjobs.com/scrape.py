from selenium import webdriver
import os
from dotenv import load_dotenv

load_dotenv()
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
import shutil, threading, sys, json

# Step 1 results
job_block_selector = ".css-1q2dra3"
job_title_selector = job_block_selector + " .css-19uc56f"
job_url_selector = job_title_selector

# Step 2
# The target HTML file name will be provided as an argument from the command line
target_html_file = sys.argv[1]

# Initialize a headless webdriver
profile_folder_path=os.getenv("CHROME_PROFILE_PATH") + os.path.sep+str(threading.get_ident())
service = ChromeService(executable_path=r""+os.getenv("CHROME_DRIVER_PATH")+"")
options = Options()
options.add_argument(f"user-data-dir={profile_folder_path}")
options.add_argument("--headless")
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")

driver = webdriver.Chrome(service=service, options=options)
driver.get(f"file:///{target_html_file}")

# Scrape all job listings using the selectors defined in Step 1
job_elements = driver.find_elements(By.CSS_SELECTOR, job_block_selector)
job_listings = [
    {"Job-title": job_element.find_element(By.CSS_SELECTOR, job_title_selector).text,
     "URL": job_element.find_element(By.CSS_SELECTOR, job_url_selector).get_attribute("href")}
    for job_element in job_elements
]

print(json.dumps(job_listings))

# Remove the folder profile_folder_path
driver.quit()
