import sys
from selenium import webdriver
import os
from dotenv import load_dotenv

load_dotenv()
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
import json
import threading

# Correct script implementation based on given instructions

def main(target_html_file):
    profile_folder_path = os.getenv("CHROME_PROFILE_PATH") + os.path.sep + str(threading.get_ident())
    service = ChromeService(executable_path=r""+os.getenv("CHROME_DRIVER_PATH")+"")
    options = webdriver.ChromeOptions()
    options.add_argument(f"user-data-dir={profile_folder_path}")
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")

    driver = webdriver.Chrome(service=service, options=options)
    driver.get(f"file:///{target_html Camdenofile}")

    # Placeholder for actual selectors from Step 1, to be replaced with the correct ones
    job_elements = driver.find_elements(By.CSS_SELECTOR, ".job-listing .job-title a")
    jobs = [{"Job-title": job_element.text, "URL": job_element.get_attribute('href')} for job_element in job_elements]

    driver.quit()

    # Return JSON representation of jobs
    return json.dumps(jobs)

if __name__ == "__main__":
    target_html_file = sys.argv[1]
    print(main(target_html_file))
