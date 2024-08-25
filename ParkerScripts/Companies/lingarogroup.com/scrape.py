import sys
from selenium import webdriver
import os
from dotenv import load_dotenv

load_dotenv()
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
import threading
import json

# The target HTML file name is received as an argument from the console
html_file_name = sys.argv[1]

def scrape_job_listings():
    profile_folder_path = f"D:\\Mind\\CRA\\AI_Experiments\\Job_Crawlers\\Peter\\adminlte-generator\\chrome_profile\\{threading.get_ident()}"
    service = ChromeService(executable_path=r""+os.getenv("CHROME_DRIVER_PATH")+"")

    options = webdriver.ChromeOptions()
    options.add_argument(f"user-data-dir={profile_folder_path}")
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")

    driver = webdriver.Chrome(service=service, options=options)
    driver.get(f'file:///{html_file_name}')

    # Find job listings based on corrected variable reference
    job_block_selector = ".jobs__item"
    job_title_selector = ".jobs__title"
    job_url_selector = "a.btn"

    job_elements = driver.find_elements(By.CSS_SELECTOR, job_block_selector)
    jobs = []
    for job_element in job_elements:
        title_element = job_element.find_element(By.CSS_SELECTOR, job_title_selector)
        url_element = job_element.find_element(By.CSS_SELECTOR, job_url_selector)
        jobs.append({"Job-title": title_element.text, "URL": url_element.get_attribute('href')})

    driver.quit()

    return json.dumps(jobs)

if __name__ == "__main__":
    job_listings_json = scrape_job_listings()
    print(job_listings_json)
