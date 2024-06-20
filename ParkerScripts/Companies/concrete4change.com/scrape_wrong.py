import sys
import json
import threading
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

def scrape_jobs(file_path):
    profile_folder_path = "D:\\Mind\\CRA\\AI_Experiments\\Job_Crawlers\\Peter\\adminlte-generator\\chrome_profile\\" + str(threading.get_ident())
    service = Service(executable_path=r"C:\Python3\chromedriver.exe")
    
    options = Options()
    options.add_argument(f"user-data-dir={profile_folder_path}")
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    
    driver = webdriver.Chrome(service=service, options=options)
    
    driver.get(f"file:///{file_path}")
    
    job_opening_selector = 'a[href*="job"], a[href*="career"], a[href*="opening"]'
    
    job_elements = driver.find_elements(By.CSS_SELECTOR, job_opening_selector)
    
    jobs = []
    for job_element in job_elements:
        title = job_element.get_attribute('textContent').strip()
        url = job_element.get_attribute('href')
        if title and url and 'http' not in url:
            jobs.append({"Job-title": title, "URL": url})
    
    driver.quit()
    
    return json.dumps(jobs, indent=4)

if __name__ == "__main__":
    file_path = sys.argv[1]
    job_listings = scrape_jobs(file_path)
    print(job_listings)