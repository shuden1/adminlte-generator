import sys
import json
import threading
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

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
        
        job_opening_selector = 'div.flex.justify-between.items-center.py-4.px-1.border-t-[1px].border-t-darker-blue'
        job_title_selector = 'span.text-light-blue.md:text-xl'
        job_url_selector = 'a[href]'
        
        job_elements = driver.find_elements(By.CSS_SELECTOR, job_opening_selector)
        job_postings = []
        
        for job_element in job_elements:
            title_element = job_element.find_element(By.CSS_SELECTOR, job_title_selector)
            url_element = job_element.find_element(By.CSS_SELECTOR, job_url_selector)
            
            title = title_element.text
            url = url_element.get_attribute('href')
            
            job_postings.append({"Job-title": title, "URL": url})
        
        print(json.dumps(job_postings, indent=4))
    
    finally:
        driver.quit()

if __name__ == "__main__":
    file_path = sys.argv[1]
    scrape_jobs(file_path)