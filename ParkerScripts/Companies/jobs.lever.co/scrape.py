import sys
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
import threading
import shutil
import json

# STEP 1: Extracted Selectors
job_block_selector = ".posting"
job_title_selector = "a.posting-title h5"
job_url_selector = "a.posting-title"

# Extracting the argument from the command line
html_file_name = sys.argv[1]

# STEP 2: Selenium Script
def get_job_listings():
    profile_folder_path = "D:\\Mind\\CRA\\AI_Experiments\\Job_Crawlers\\Peter\\adminlte-generator\\chrome_profile\\" + str(threading.get_ident())

    service = ChromeService(executable_path=r"C:\Python3\chromedriver.exe")
    options = webdriver.ChromeOptions()
    options.add_argument(f"user-data-dir={profile_folder_path}")
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")

    driver = webdriver.Chrome(service=service, options=options)
    driver.get(f"file:///{html_file_name}")

    job_blocks = driver.find_elements(By.CSS_SELECTOR, job_block_selector)
    job_listings = []

    for job_block in job_blocks:
        title_element = job_block.find_element(By.CSS_SELECTOR, job_title_selector)
        title = title_element.text
        url_element = job_block.find_element(By.CSS_SELECTOR, job_url_selector)
        url = url_element.get_attribute('href')
        job_listings.append({"Job-title": title, "URL": url})

    driver.quit()

    return json.dumps(job_listings)

# Call the function and print the JSON
print(get_job_listings())
