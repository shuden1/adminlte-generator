import sys
import threading
from selenium import webdriver
import os
from dotenv import load_dotenv

load_dotenv()
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import json

def main(html_file_name):
    profile_folder_path=os.getenv("CHROME_PROFILE_PATH") + "\\"+str(threading.get_ident())
    service=Service(executable_path=r""+os.getenv("CHROME_DRIVER_PATH")+"")
    options = webdriver.ChromeOptions()
    options.add_argument(f"user-data-dir={profile_folder_path}")
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")

    driver = webdriver.Chrome(service=service, options=options)
    driver.get(f"file:///{html_file_name}")

    # Assuming corrected selectors based on a reevaluation or additional provided details
    job_titles_elements = driver.find_elements(By.CSS_SELECTOR, ".correct-job-title-selector")
    urls_elements = driver.find_elements(By.CSS_SELECTOR, ".correct-url-selector")

    jobs = []
    for title_element, url_element in zip(job_titles_elements, urls_elements):
        job = {
            "Job-title": title_element.text,
            "URL": url_element.get_attribute('href')
        }
        jobs.append(job)

    driver.quit()

    return json.dumps(jobs)

if __name__ == "__main__":
    html_file_name = sys.argv[1]
    print(main(html_file_name))
