import sys
from selenium.webdriver import Chrome, ChromeOptions
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
import threading
import shutil
import json

# Retrieve the HTML file name from the argument passed through the console
html_file = sys.argv[1]

# Initialising a headless webdriver with profile path
profile_folder_path = os.getenv("CHROME_PROFILE_PATH") + os.path.sep + str(threading.get_ident())
service = ChromeService(executable_path=r""+os.getenv("CHROME_DRIVER_PATH")+"")
options = ChromeOptions()
options.add_argument(f"user-data-dir={profile_folder_path}")
options.add_argument("--headless")
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")
driver = Chrome(service=service, options=options)

# Open the HTML file
driver.get(f"file:///{html_file}")

# Selectors identified in STEP 1
job_block_selector = '.table_basic-1.table_striped.table_overflow tbody tr'
job_title_selector = 'td[data-th="Job Title"] a'

# Scrape all job listings
jobs = []
elements = driver.find_elements(By.CSS_SELECTOR, job_block_selector)
for element in elements:
    job_title_element = element.find_element(By.CSS_SELECTOR, job_title_selector)
    job_title = job_title_element.text
    job_url = job_title_element.get_attribute('href')
    jobs.append({"Job-title": job_title, "URL": job_url})

# Return a JSON in the requested format
print(json.dumps(jobs))

# Close the browser and delete the profile folder
driver.quit()
