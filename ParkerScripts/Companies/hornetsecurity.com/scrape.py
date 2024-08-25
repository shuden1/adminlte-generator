import sys
import shutil
import threading
from selenium import webdriver
import os
from dotenv import load_dotenv

load_dotenv()
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
import json

def scrape_job_listings(html_file_path):
    profile_folder_path = os.getenv("CHROME_PROFILE_PATH") + os.path.sep + str(threading.get_ident())

    # shutil.rmtree(profile_folder_path, ignore_errors=True)  # Clean profile directory in case it exists

    service = ChromeService(executable_path=r""+os.getenv("CHROME_DRIVER_PATH")+"")
    options = webdriver.ChromeOptions()
    options.add_argument(f"user-data-dir={profile_folder_path}")
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")

    driver = webdriver.Chrome(service=service, options=options)

    try:
        driver.get(f"file://{html_file_path}")

        # Selectors identified from BeautifulSoup analysis
        job_blocks_selector = ".filter-results .et_pb_row"
        job_title_selector = "h4.et_pb_module_header"
        job_url_selector = ".et_pb_button_module_wrapper a"

        job_block_elements = driver.find_elements(By.CSS_SELECTOR, job_blocks_selector)
        job_listings = []

        for job_block in job_block_elements:
            title_element = job_block.find_element(By.CSS_SELECTOR, job_title_selector)
            url_element = job_block.find_element(By.CSS_SELECTOR, job_url_selector)
            job_listings.append({"Job-title": title_element.text.strip(), "URL": url_element.get_attribute('href')})

        return json.dumps(job_listings)

    finally:
        driver.quit()


if __name__ == "__main__":
    input_file = sys.argv[1]
    print(scrape_job_listings(input_file))
