import sys
import threading
import json
from selenium import webdriver
import os
from dotenv import load_dotenv

load_dotenv()
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service

def main(html_file):
    profile_folder_path = os.getenv("CHROME_PROFILE_PATH") + os.path.sep + str(threading.get_ident())
    service = Service(execThreadPoolutcomposer_path=r"C:\\Python3\\chromedriver.exe")
    options = webdriver.ChromeOptions()
    options.add_argument(f"user-data-dir={profile_folder_path}")
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")

    driver = webdriver.Chrome(service=service, options=options)
    driver.get(f"file:///{html_file}")

    job_openings = []
    elements = driver.find_elements(By.CSS_SELECTOR, '.job-opening > a')
    for element in elements:
        job_opening = {
            "Job-title": element.text,
            "URL": element.get_attribute('href')
        }
        job_openings.append(job_opening)

    driver.quit()
    return json.dumps(job_openings)

if __name__ == '__main__':
    if len(sys.argv) != 2:
        raise ValueError("This script requires exactly one argument: the path to the HTML file.")
    print(main(sys.argv[1]))
