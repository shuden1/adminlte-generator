from selenium import webdriver
from selenium.webdriver.common.by import By
import json
import sys
import threading

# Retrieve the filename of the HTML file from command line arguments
filename = sys.argv[1]

# Selenium WebDriver setup with headless Chrome
profile_folder_path = "D:\\Mind\\CRA\\AI_Experiments\\Job_Crawlers\\Peter\\adminlte-generator\\chrome_profile\\" + str(threading.get_ident())
options = webdriver.ChromeOptions()
options.add_argument(f"user-data-dir={profile_folder_path}")
options.add_argument("--headless")
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")

service = webdriver.chrome.service.Service(executable_path=r"C:\Python3\chromedriver.exe")
driver = webdriver.Chrome(service=service, options=options)

# Load the HTML file
driver.get(f"file://{filename}")

# Define the exact selectors for job blocks, titles, and URLs
job_blocks_selector = ".about-us-col div.full"
title_selector = "p"

# Scrape the job listings
job_blocks = driver.find_elements(By.CSS_SELECTOR, job_blocks_selector)
jobs = []

for block in job_blocks:
    job_title_elements = block.find_elements(By.CSS_SELECTOR, title_selector)

    for job_elem in job_title_elements:
        # The expected format for job title and link here is the inner text and the email respectively
        job_title = job_elem.text
        job_link = "mailto:JOBS@MURKA.COM"

        jobs.append({"Job-title": job_title, "URL": job_link})

# Quit the driver
driver.quit()

# Output job listings as JSON
print(json.dumps(jobs))