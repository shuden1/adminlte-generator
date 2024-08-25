import sys
import json
import threading
from selenium import webdriver
import os
from dotenv import load_dotenv

load_dotenv()
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

def main(html_file_path):
    profile_folder_path = f"D:\\Mind\\CRA\\AI_Experiments\\Job_Crawlers\\Peter\\adminlte-generator\\chrome_profile\\{str(threading.get_ident())}"
    service_path = r""+os.getenv("CHROME_DRIVER_PATH")+""
    service = Service(executable_path=service_path)
    options = Options()
    options.add_argument(f"user-data-dir={profile_folder_path}")
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")

    driver = webdriver.Chrome(service=service, options=options)
    driver.get(f"file:///{html_file_path}")

    # Placeholder for actual job listing selectors based on the HTML file structure
    job_listing_selectors = "PLEASE_REPLACE_WITH_ACTUAL_SELECTORS_BASED_ON_HTML_STRUCTURE"
    job_title_selectors = "PLEASE_REPLACE_WITH_ACTUAL_SELECTORS_BASED_ON_HTML_STRUCTURE"
    job_url_selectors = "PLEASE_REPLACE_WITH_ACTUAL_SELECTORS_BASED_ON_HTML_STRUCTURE"

    # Assuming job listings are in a certain structure that needs the actual selectors to be replaced above
    job_listings = driver.find_elements(By.CSS_SELECTOR, job_listing_selectors)
    result = []

    for job_listing in job_listings:
        job_title = job_listing.find_element(By.CSS_SELECTOR, job_title_selectors).text
        job_url = job_listing.find_element(By.CSS_SELECTOR, job_url_selectors).get_attribute('href')
        result.append({"Job-title": job_title, "URL": job_url})

    driver.quit()

    print(json.dumps(result))

if __name__ == "__main__":
    html_file_path = sys.argv[1]
    main(html_file_path)
