import sys
from selenium import webdriver
import os
from dotenv import load_dotenv

load_dotenv()
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
import threading
import json

# Initialization of the headless ChromeDriver
profile_folder_path = os.getenv("CHROME_PROFILE_PATH") + os.path.sep + str(threading.get_ident())
service = ChromeService(executable_path=r""+os.getenv("CHROME_DRIVER_PATH")+"")
options = webdriver.ChromeOptions()
options.add_argument(f"user-data-dir={profile_folder_path}")
options.add_argument("--headless")
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")

# Starting the browser
driver = webdriver.Chrome(service=service, options=options)

def scrape_job_listings(file_name):
    # Opening the file as provided by the argument from the external source
    driver.get(f"file:///{file_title}")

    # Scraping job titles and URLs
    jobs_data = []
    job_elements = driver.find_elements(By.CSS_SELECTOR, ".job-innerwrap")
    for job_element in job_elements:
        title_element = job_element.find_element(By.CSS_SELECTOR, ".jobTitle a")
        title = title_element.text
        url = title_element.get_attribute('href')
        jobs_data.append({"Job-title": title, "URL": url})

    driver.quit()
    print(json.dumps(jobs_data))

if __name__ == "__main__":
    file_title = sys.argv[1]
    scrape_job_listings(file_title)
