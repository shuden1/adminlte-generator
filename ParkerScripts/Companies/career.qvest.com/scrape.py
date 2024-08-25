import sys
from selenium import webdriver
import os
from dotenv import load_dotenv

load_dotenv()
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
import threading
import json

# The target HTML file name from the command line argument
target_html = sys.argv[1]

# ChromeDriver setup
service = ChromeService(executable_path=r""+os.getenv("CHROME_DRIVER_PATH")+"")
profile_folder_path=os.getenv("CHROME_PROFILE_PATH") + os.path.sep+str(threading.get_ident())
options = webdriver.ChromeOptions()
options.add_argument(f"user-data-dir={profile_folder_path}")
options.add_argument("--headless")
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")

# Initialize the WebDriver
driver = webdriver.Chrome(service=service, options=options)

# Open the target HTML file
driver.get(f"file:///{target_html}")

# Define selectors based on step 1 analysis
selectors = {
    "job_blocks": "td.link",  # Selector for job opening blocks
    "job_titles": "a",  # Selector for job titles
}

# Scrape job titles and their URLs
jobs = []
for job_element in driver.find_elements(By.CSS_SELECTOR, selectors["job_blocks"]):
    job_title_element = job_element.find_element(By.CSS_SELECTOR, selectors["job_titles"])
    job_title = job_title_element.text.strip()
    job_url = job_title_element.get_attribute('href')
    jobs.append({"Job-title": job_title, "URL": job_url})

# Output the result
print(json.dumps(jobs))

# Close the WebDriver
driver.quit()
