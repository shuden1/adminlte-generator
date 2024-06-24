import sys
import json
import threading
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException

def scrape_jobs(file_path):
    profile_folder_path = "D:\\Mind\\CRA\\AI_Experiments\\Job_Crawlers\\Peter\\adminlte-generator\\chrome_profile\\" + str(threading.get_ident())
    service = Service(executable_path=r"C:\Python3\chromedriver.exe")
    
    options = webdriver.ChromeOptions()
    options.add_argument(f"user-data-dir={profile_folder_path}")
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    
    driver = webdriver.Chrome(service=service, options=options)
    
    try:
        driver.get(f"file:///{file_path}")
        
        job_openings = []
        
        job_elements = driver.find_elements(By.CSS_SELECTOR, "div.job-ad-card-wrapper[role='document']")
        
        for job_element in job_elements:
            try:
                title_element = job_element.find_element(By.CSS_SELECTOR, "h2.title.job-ad-card__description-title")
                title = title_element.text.strip() if title_element.text.strip() else title_element.get_attribute('innerHTML').strip()
            except NoSuchElementException:
                title = "No Title"
            
            try:
                url_element = job_element.find_element(By.CSS_SELECTOR, "a.link[data-link-lv='jobs_link']")
                url = url_element.get_attribute('href').strip() if url_element.get_attribute('href').strip() else "#"
            except NoSuchElementException:
                url = "#"
            
            job_openings.append({"Job-title": title, "URL": url})
        
        print(json.dumps(job_openings, ensure_ascii=False, indent=4))
    
    finally:
        driver.quit()

if __name__ == "__main__":
    file_path = sys.argv[1]
    scrape_jobs(file_path)