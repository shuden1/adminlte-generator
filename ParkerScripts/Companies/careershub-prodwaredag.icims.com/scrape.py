import sys
from selenium import webdriver
import os
from dotenv import load_dotenv

load_dotenv()
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import json
import threading

# Step 1 outcomes
job_block_selector = ".container-fluid.iCIMS_JobsTable .row"
job_title_selector = ".title a h3"
job_url_selector = ".title a"

def scrape_job_listings(file_name):
    profile_folder_path = os.getenv("CHROME_PROFILE_PATH") + "\\" + str(threading.get_ident())
    options = webdriver.ChromeOptions()
    options.add_argument(f"user-data-dir={profile_folder_path}")
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    chrome_service = Service(executable_path=r""+os.getenv("CHROME_DRIVER_PATH")+"")
    driver = webdriver.Chrome(service=chrome_service, options=options)

    driver.get(f"file:///{file_name}")

    job_listings = []
    job_elements = driver.find_elements(By.CSS_SELECTOR, job_block_selector)
    for job_element in job_elements:
        title = job_element.find_element(By.CSS_SELECTOR, job_title_selector).text
        url = job_element.find_element(By.CSS_SELECTOR, job_url_selector).get_attribute('href')
        job_listings.append({"Job-title": title, "URL": url})

    driver.quit()
    return json.dumps(job_listings)

if __name__ == "__main__":
    file_name = sys.argv[1]

    print(scrape_job_listings(file_name))
