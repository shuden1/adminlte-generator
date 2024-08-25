import sys
from selenium import webdriver
import os
from dotenv import load_dotenv

load_dotenv()
from selenium.webdriver.common.by import By
import threading
import json

def scrape_jobs(html_file_path):
    profile_folder_path = os.getenv("CHROME_PROFILE_PATH") + "\\" + str(threading.get_ident())
    options = webdriver.ChromeOptions()
    options.add_argument(f"user-data-dir={profile_folder_path}")
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    service = webdriver.chrome.service.Service(executable_path=r""+os.getenv("CHROME_DRIVER_PATH")+"")

    driver = webdriver.Chrome(service=service, options=options)
    driver.get(f"file:///{html_file_path}")

    jobs = []
    job_elements = driver.find_elements(By.CSS_SELECTOR, ".et_pb_promo_description p, .et_pb_promo_description li")
    for job_element in job_elements:
        job_title = job_element.text
        job_url = "mailto:jobs@beatshapers.com"  # URL is the same for all job listings in this case
        jobs.append({"Job-title": job_title, "URL": job_url})

    driver.quit()
    return json.dumps(jobs, ensure_ascii=False)

if __name__ == "__main__":
    html_file_path = sys.argv[1]
    print(scrape_jobs(html_file_path))
