import sys
from selenium import webdriver
import os
from dotenv import load_dotenv

load_dotenv()
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
import threading
import json

# Assuming the input parameter is the filepath to the target HTML file
target_html_file = sys.argv[1]

# Selenium WebDriver initialization with headless configuration
profile_folder_path = os.getenv("CHROME_PROFILE_PATH") + "\\" + str(threading.get_ident())
service = ChromeService(executable_path=r""+os.getenv("CHROME_DRIVER_PATH")+"")
options = webdriver.ChromeOptions()
options.add_argument("--headless")
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")
options.add_argument(f"user-data-dir={profile_folder_path}")

driver = webdriver.Chrome(service=service, options=options)

# Opening the local HTML file
driver.get(f"file:///{target_html_file}")

# Corrected scraping logic
# Replace '.career__vacancy a' with the correct selector if it was inaccurately identified previously.
# Ensure this selector targets only the meaningful links associated with job postings.
job_elements = driver.find_elements(By.CSS_SELECTOR, ".career__vacancy a[href]")
jobs = []

for job_element in job_elements:
    title = job_element.text.strip()
    url = job_element.get_attribute('href').strip()
    if title and url.startswith("http"):
        jobs.append({"Job-title": title, "URL": url})

driver.quit()

# Output the jobs in JSON format
print(json.dumps(jobs))
