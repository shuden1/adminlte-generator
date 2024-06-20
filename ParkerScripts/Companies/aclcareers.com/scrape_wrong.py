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
        
        job_blocks = driver.find_elements(By.CSS_SELECTOR, 'div[class*="job"], ul[class*="job"] > li')
        
        job_postings = []
        for block in job_blocks:
            title_tag = block.find_element(By.CSS_SELECTOR, 'a, h2 a, h3 a, p a')
            if title_tag:
                job_postings.append({
                    'Job-title': title_tag.text.strip(),
                    'URL': title_tag.get_attribute('href')
                })
        
        print(json.dumps(job_postings, indent=4))
    
    finally:
        driver.quit()

if __name__ == "__main__":
    file_path = sys.argv[1]
    scrape_jobs(file_path)