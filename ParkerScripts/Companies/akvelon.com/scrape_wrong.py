import sys
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import json
import threading

def scrape_jobs(file_path):
    profile_folder_path = "D:\\Mind\\CRA\\AI_Experiments\\Job_Crawlers\\Peter\\adminlte-generator\\chrome_profile\\" + str(threading.get_ident())
    service = Service(executable_path=r"C:\Python3\chromedriver.exe")
    options = webdriver.ChromeOptions()
    options.add_argument(f"user-data-dir={profile_folder_path}")
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")

    driver = webdriver.Chrome(service=service, options=options)
    driver.get("file:///" + file_path)

    # Adjust these selectors based on actual page structure
    jobs = driver.find_elements(By.CSS_SELECTOR, '.job-listing .job-title a')

    job_listings = []
    for job in jobs:
        job_title = job.text
        job_url = job.get_attribute('href')
        job_listings.append({"Job-title": job_title, "URL": job_url})

    driver.quit()
    
    print(json.dumps(job_listings))

if __name__ == "__main__":
    file_name = sys.argv[1]
    scrape_jobs(file_name)