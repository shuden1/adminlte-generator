import sys
import json
import shutil
import threading
from selenium import webdriver
import os
from dotenv import load_dotenv

load_dotenv()
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By

# STEP 1 results: the selectors as identified from the BeautifulSoup process
job_block_selector = ".job-card.row.mx-4.mx-md-0"
job_title_selector = ".job-title.text-center.text-md-start"
job_url_selector = "a.btn.btn-outline-primary"

# STEP 2: Selenium script
def scrape_job_listings(html_file_name):
    profile_folder_path = os.getenv("CHROME_PROFILE_PATH") + os.path.sep + str(threading.get_ident())
    service = ChromeService(executable_path=r""+os.getenv("CHROME_DRIVER_PATH")+"")
    options = webdriver.ChromeOptions()
    options.add_argument(f"user-data-dir={profile_folder_path}")
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")

    driver = webdriver.Chrome(service=service, options=options)
    driver.get(f"file:///{html_file_name}")

    job_listings = []
    job_blocks = driver.find_elements(By.CSS_SELECTOR, job_block_selector)
    for job_block in job_blocks:
        title_element = job_block.find_element(By.CSS_SELECTOR, job_title_selector)
        url_element = job_block.find_element(By.CSS_SELECTOR, job_url_selector)
        job_listings.append({"Job-title": title_element.text, "URL": url_element.get_attribute('href')})

    driver.quit()

    return json.dumps(job_listings)

if __name__ == "__main__":
    html_file_name = sys.argv[1]
    print(scrape_job_listings(html_file_name))
