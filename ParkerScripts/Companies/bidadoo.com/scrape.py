import sys
import json
import threading
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
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
        
        job_openings = driver.find_elements(By.CSS_SELECTOR, 'div[style*="background-color: transparent; color: #000000; font-family: Verdana,Arial,Helvetica,sans-serif; font-size: 14px; font-style: normal; font-variant: normal; font-weight: 400; letter-spacing: normal; line-height: 21px; min-height: 0px; orphans: 2; text-align: left; text-decoration: none; text-indent: 0px; text-transform: none; -webkit-text-stroke-width: 0px; white-space: normal; word-spacing: 0px;"]')
        
        job_listings = []
        
        for job in job_openings:
            try:
                title_element = job.find_element(By.CSS_SELECTOR, 'a[rel="noopener noreferrer"][target="_blank"]')
                title = title_element.text.strip() if title_element.text.strip() else title_element.get_attribute('innerHTML').strip()
                url = title_element.get_attribute('href') if title_element.get_attribute('href') else "#"
                
                job_listings.append({"Job-title": title, "URL": url})
            except NoSuchElementException:
                continue
        
        print(json.dumps(job_listings, indent=4))
    
    finally:
        driver.quit()

if __name__ == "__main__":
    file_path = sys.argv[1]
    scrape_jobs(file_path)