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
        
        job_opening_selector = 'div[class*="job"], ul[class*="job"] > li, div[class*="opening"], ul[class*="opening"] > li, div[class*="career"], ul[class*="career"] > li, div[class*="position"], ul[class*="position"] > li'
        job_title_selector = 'a, h2 > a, h3 > a, p > a'
        
        job_blocks = driver.find_elements(By.CSS_SELECTOR, job_opening_selector)
        job_postings = []
        
        for block in job_blocks:
            title_element = block.find_element(By.CSS_SELECTOR, job_title_selector)
            job_postings.append({
                "Job-title": title_element.text,
                "URL": title_element.get_attribute("href")
            })
        
        print(json.dumps(job_postings, indent=4))
    
    finally:
        driver.quit()

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script.py <path_to_html_file>")
        sys.exit(1)
    
    file_path = sys.argv[1]
    scrape_jobs(file_path)