import sys
import threading
from selenium import webdriver
import os
from dotenv import load_dotenv

load_dotenv()
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service

# The filename should be an argument sent from an external source through the console command
html_file_name = sys.argv[1]

# Setting up the Chrome webdriver with specified options and profile path
profile_folder_path = os.getenv("CHROME_PROFILE_PATH") + "\\" + str(threading.get_ident())
service = Service(executable_path=r""+os.getenv("CHROME_DRIVER_PATH")+"")
options = webdriver.ChromeOptions()
options.add_argument(f"user-data-dir={profile_folder_path}")
options.add_argument("--headless")
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")

# Initializing the webdriver
driver = webdriver.Chrome(service=service, options=options)

# Opening the target HTML file
driver.get("file:///" + html_file_name)

# Identifying job listings using the selectors from STEP 1
job_openings_blocks = driver.find_elements(By.CSS_SELECTOR, "div.LayoutContainer_container__SqT4a.PageCareersPositionsBrowse_vacanciesBlock__hAA7e")

# Extracting job titles and their URLs, excluding mailto links
jobs = []

for block in job_openings_blocks:
    job_links = block.find_elements(By.CSS_SELECTOR, "a")
    for link in job_links:
        job_url = link.get_attribute("href")
        if "mailto:" not in job_url:
            job_title = link.text
            jobs.append({"Job-title": job_title, "URL": job_url})

# Closing the driver
driver.quit()

# Printing the job listings as JSON
print(jobs)
