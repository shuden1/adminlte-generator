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
        
        job_elements = driver.find_elements(By.CSS_SELECTOR, "div.card.position-card.pointer")
        job_listings = []
        
        for job_element in job_elements:
            job_title_element = job_element.find_element(By.CSS_SELECTOR, "div.position-title.line-clamp.line-clamp-2")
            job_title = job_title_element.text
            
            job_url = "#"  # Default to "#" if no URL is found within the job element
            
            job_listings.append({"Job-title": job_title, "URL": job_url})
        
        print(json.dumps(job_listings, indent=4))
    
    finally:
        driver.quit()

if __name__ == "__main__":
    file_path = sys.argv[1]
    scrape_jobs(file_path)