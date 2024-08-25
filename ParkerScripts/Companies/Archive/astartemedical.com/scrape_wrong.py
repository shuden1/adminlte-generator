from selenium import webdriver
import os
from dotenv import load_dotenv

load_dotenv()
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import json
import sys

def scrape_job_openings(html_file):
    service = Service(ChromeDriverManager().install())
    options = webdriver.ChromeOptions()
    options.headless = True
    driver = webdriver.Chrome(service=service, options=options)

    driver.get("file:///" + html_file)

    jobs = []
    job_elements = driver.find_elements(By.CSS_SELECTOR, ".elementor-widget-container .elementor-heading-title.elementor-size-default a")

    for job_element in job_elements:
        job_title = job_element.text
        job_url = job_element.get_attribute('href')
        jobs.append({"Job-title": job_title, "URL": job_url})

    driver.quit()
    return json.dumps(jobs)

if __name__ == "__main__":
    html_file = sys.argv[1]
    print(scrape_job_openings(html_file))
