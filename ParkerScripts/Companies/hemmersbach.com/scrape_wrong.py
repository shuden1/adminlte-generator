import sys
import json
import threading
from selenium import webdriver
import os
from dotenv import load_dotenv

load_dotenv()
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service

def main(target_html_file):
    profile_folder_path = f"{os.getenv("CHROME_PROFILE_PATH")}{os.path.sep}{threading.get_ident()}"

    options = webdriver.ChromeOptions()
    options.add_argument(f"user-data-dir={profile_folder_path}")
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")

    service = Service(executable_path=r""+os.getenv("CHROME_DRIVER_PATH")+"")
    driver = webdriver.Chrome(service=service, options=options)

    driver.get(f"file:///{target_html_file}")

    # Placeholder selectors; replace with actual selectors identified in step 1
    job_listings = []
    try:
        for job_block in driver.find_elements(By.CSS_SELECTOR, "REPLACE_WITH_JOB_BLOCK_SELECTOR"):
            title = job_block.find_element(By.CSS_SELECTOR, "REPLACE_WITH_JOB_TITLE_SELECTOR").text
            url = job_block.find_element(By.CSS_SELECTOR, "REPLACE_WITH_JOB_URL_SELECTOR").get_attribute('href')
            job_listings.append({"Job-title": title, "URL": url})
    except Exception:
        pass

    driver.quit()

    print(json.dumps(job_listings))

if __name__ == "__main__":
    main(sys.argv[1])
