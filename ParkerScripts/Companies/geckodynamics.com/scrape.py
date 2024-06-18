import sys
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
import threading
import json

# Get HTML file name from command line argument
html_file_name = sys.argv[1]

# Define selectors based on STEP 1 analysis
job_block_selector = ".jobs-list .jobs-item"
job_title_selector = ".jobs-item__title"
job_url_selector = ".jobs-list .jobs-item"

# WebDriver configuration
profile_folder_path="D:\\Mind\\CRA\\AI_Experiments\\Job_Crawlers\\Peter\\adminlte-generator\\chrome_profile\\"+str(threading.get_ident())
service = ChromeService(executable_path=r"C:\Python3\chromedriver.exe")
options = webdriver.ChromeOptions()
options.add_argument(f"user-data-dir={profile_folder_path}")
options.add_argument("--headless")
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")

def scrape_jobs():
    # Initialize WebDriver
    driver = webdriver.Chrome(service=service, options=options)
    driver.get(f"file:///{html_file_name}")

    # Find job listings based on selectors
    job_elements = driver.find_elements(by=By.CSS_SELECTOR, value=job_block_selector)
    job_list = []

    for job_element in job_elements:
        job_title = job_element.find_element(by=By.CSS_SELECTOR, value=job_title_selector).text
        job_url = job_element.get_attribute('href')
        job_list.append({"Job-title": job_title, "URL": job_url})

    driver.quit()

    # Return json data
    return json.dumps(job_list)

# Invoke function to scrape jobs
print(scrape_jobs())