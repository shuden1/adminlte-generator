from selenium import webdriver
import os
from dotenv import load_dotenv

load_dotenv()
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import json
import sys
import threading

# Extracting the target HTML file name from the command line argument
file_name = sys.argv[1]

# Setting up the Chrome driver with specified options
profile_folder_path = f"D:\\Mind\\CRA\\AI_Experiments\\Job_Crawlers\\Peter\\adminlte-generator\\chrome_profile\\{str(threading.get_ident())}"
service = Service(executable_path=r""+os.getenv("CHROME_DRIVER_PATH")+"")
options = webdriver.ChromeOptions()
options.add_argument(f"user-data-dir={profile_folder_path}")
options.add_argument("--headless")
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")

# Initiating the driver
driver = webdriver.Chrome(service=service, options=options)

try:
    # Loading the specified HTML file
    driver.get(f"file:///{file_name}")

    # Finding elements by CSS selectors based on the clues got before
    jobs = driver.find_elements(By.CSS_SELECTOR, "li[class^='job-tile']")  # Adjusted class selector

    job_listings = []

    for job in jobs:
        # Finding job titles and URLs within each job block
        title_element = job.find_element(By.CSS_SELECTOR, "span[class='col-md-12 section-title title'] a")
        title = title_element.text.strip()
        url = title_element.get_attribute('href')

        job_listings.append({"Job-title": title, "URL": url})

    # Outputting the job listings in JSON format
    print(json.dumps(job_listings, ensure_ascii=False))

finally:
    # Clean up by closing the driver
    driver.quit()
