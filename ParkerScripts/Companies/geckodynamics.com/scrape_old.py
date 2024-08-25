from selenium import webdriver
import os
from dotenv import load_dotenv

load_dotenv()
from selenium.webdriver.common.by import By
import json
import sys
import threading

def scrape_job_listings():
    file_path = sys.argv[1]

    profile_folder_path = f"{os.getenv("CHROME_PROFILE_PATH")}{os.path.sep}{threading.get_ident()}"
    service = webdriver.ChromeService(executable_path=r""+os.getenv("CHROME_DRIVER_PATH")+"")
    options = webdriver.ChromeOptions()
    options.add_argument(f"user-data-dir={profile_folder_path}")
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")

    driver = webdriver.Chrome(service=service, options=options)
    driver.get(f"file:///{file_path}")

    job_elements = driver.find_elements(By.CSS_SELECTOR, ".jobs-list .jobs-item")
    jobs_data = []

    for job_element in job_elements:
        try:
            title_element = job_element.find_element(By.CSS_SELECTOR, ".jobs-item__title")
            job_title = title_element.text
            if job_title and not job_title.startswith("Don’t see the dream job"):
                url = job_element.get_attribute("href")
                jobs_data.append({"Job-title": job_title, "URL": url})
        except:
            continue

    driver.quit()

    return json.dumps(jobs_data)

if __name__ == "__main__":
    print(scrape_job_listings())
