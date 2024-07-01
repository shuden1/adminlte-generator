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
        
        job_listings = []
        
        job_elements = driver.find_elements(By.CSS_SELECTOR, "li.w-full")
        
        for job_element in job_elements:
            try:
                title_element = job_element.find_element(By.CSS_SELECTOR, "span.text-block-base-link.sm\\:min-w-\\[25\\%\\].sm\\:truncate.company-link-style")
                title = title_element.text.strip() or title_element.get_attribute('innerHTML').strip()
            except NoSuchElementException:
                title = "No Title"
            
            try:
                url_element = job_element.find_element(By.CSS_SELECTOR, "a.flex.flex-col.py-6.text-center.sm\\:px-6.hover\\:bg-gradient-block-base-bg.focus-visible-company.focus-visible\\:rounded")
                url = url_element.get_attribute('href') or "#"
            except NoSuchElementException:
                url = "#"
            
            job_listings.append({"Job-title": title, "URL": url})
        
        print(json.dumps(job_listings, indent=4))
    
    finally:
        driver.quit()

if __name__ == "__main__":
    file_path = sys.argv[1]
    scrape_jobs(file_path)