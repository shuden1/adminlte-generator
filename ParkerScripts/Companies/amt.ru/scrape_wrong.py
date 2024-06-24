import sys
import json
import threading
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException

def scrape_jobs(file_path):
    profile_folder_path = "D:\\Mind\\CRA\\AI_Experiments\\Job_Crawlers\\Peter\\adminlte-generator\\chrome_profile\\" + str(threading.get_ident())
    service = Service(executable_path=r"C:\Python3\chromedriver.exe")
    
    options = Options()
    options.add_argument(f"user-data-dir={profile_folder_path}")
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    
    driver = webdriver.Chrome(service=service, options=options)
    
    try:
        driver.get(f"file:///{file_path}")
        
        job_openings = driver.find_elements(By.CSS_SELECTOR, "li")
        jobs = []
        
        for job in job_openings:
            try:
                job_title_element = job.find_element(By.CSS_SELECTOR, "a[href]")
                job_title = job_title_element.text.strip() or job_title_element.get_attribute('innerHTML').strip()
                job_url = job_title_element.get_attribute('href') or "#"
                
                jobs.append({"Job-title": job_title, "URL": job_url})
            except NoSuchElementException:
                continue
        
        print(json.dumps(jobs, ensure_ascii=False))
    
    finally:
        driver.quit()

if __name__ == "__main__":
    file_path = sys.argv[1]
    scrape_jobs(file_path)