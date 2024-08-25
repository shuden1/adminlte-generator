import sys
import json
from selenium import webdriver
import os
from dotenv import load_dotenv

load_dotenv()
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
import shutil
import threading

# STEP 2: Selenium script

# The input is the file name passed as the first argument from the command line
file_name = sys.argv[1]

# Corrected selectors based on BeautifulSoup analysis
selector_job_block = "div.bg-fire-burst div.bg-white"
selector_job_title = "h3.mb-2"
selector_job_url = "div.btn-secondary-sm a"

def main(file_name):
    profile_folder_path = os.getenv("CHROME_PROFILE_PATH") + "\\"+str(threading.get_ident())
    service = ChromeService(executable_path=r""+os.getenv("CHROME_DRIVER_PATH")+"")
    options = Options()
    options.add_argument(f"user-data-dir={profile_folder_path}")
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")

    driver = webdriver.Chrome(service=service, options=options)
    driver.get(f"file:///{file_name}")

    job_blocks = driver.find_elements(By.CSS_SELECTOR, selector_job_block)
    job_listings = []
    for job_block in job_blocks:
        title = job_block.find_element(By.CSS_SELECTOR, selector_job_title).text.strip()
        url = job_block.find_element(By.CSS_SELECTOR, selector_job_url).get_attribute('href').strip()
        job_listings.append({"Job-title": title, "URL": url})

    driver.quit()


    return json.dumps(job_listings)

# Only to structure code, remove or comment out when running through console
if __name__ == "__main__":
    file_name = sys.argv[1]
    print(main(file_name))
