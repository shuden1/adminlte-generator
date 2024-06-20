import sys
import json
import threading
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

def scrape_job_listings(html_file_path):
    profile_folder_path = "D:\\Mind\\CRA\\AI_Experiments\\Job_Crawlers\\Peter\\adminlte-generator\\chrome_profile\\" + str(threading.get_ident())
    service = Service(executable_path=r"C:\Python3\chromedriver.exe")
    
    options = Options()
    options.add_argument(f"user-data-dir={profile_folder_path}")
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    
    driver = webdriver.Chrome(service=service, options=options)
    
    try:
        driver.get(f"file:///{html_file_path}")
        
        job_openings = []
        
        job_blocks = driver.find_elements(By.CSS_SELECTOR, 'div.job-selector.job-list')
        for job_block in job_blocks:
            title_element = job_block.find_element(By.CSS_SELECTOR, 'div.job-list-title')
            url_element = job_block.find_element(By.CSS_SELECTOR, 'a.a-cta')
            
            job_title = title_element.text.strip()
            job_url = url_element.get_attribute('href')
            
            job_openings.append({"Job-title": job_title, "URL": job_url})
        
        print(json.dumps(job_openings, indent=4))
    
    finally:
        driver.quit()

if __name__ == "__main__":
    html_file_path = sys.argv[1]
    scrape_job_listings(html_file_path)