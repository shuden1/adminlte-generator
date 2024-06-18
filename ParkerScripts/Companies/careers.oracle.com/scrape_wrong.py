import sys
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import json
import threading

def scrape_job_listings(html_file_path):
    profile_folder_path = "D:\\Mind\\CRA\\AI_Experiments\\Job_Crawlers\\Peter\\adminlte-generator\\chrome_profile\\" + str(threading.get_ident())
    service = Service(executable_path=r"C:\Python3\chromedriver.exe")
    options = Options()
    options.add_argument(f"user-data-dir={profile_folder_path}")
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")

    driver = webdriver.Chrome(service=service, options=options)
    driver.get(f"file:///{html_file_path}")

    # Replace the CSS SELECTORS based on the analysis made in STEP 1
    job_elements = driver.find_elements(By.CSS_SELECTOR, "REPLACE_WITH_JOB_BLOCK_SELECTOR")
    jobs = []
    for job_element in job_elements:
        job_title = job_element.find_element(By.CSS_SELECTOR, "REPLACE_WITH_JOB_TITLE_SELECTOR").text
        job_url = job_element.find_element(By.CSS_SELECTOR, "REPLACE_WITH_JOB_URL_SELECTOR").get_attribute('href')
        jobs.append({"Job-title": job_title, "URL": job_url})
    
    driver.quit()
    return jobs

if __name__ == "__main__":
    target_html_file = sys.argv[1]
    job_listings = scrape_job_listings(target_html_file)
    print(json.dumps(job_listings))