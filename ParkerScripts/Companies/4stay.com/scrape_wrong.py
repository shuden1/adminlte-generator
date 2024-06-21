import sys
import json
import threading
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

def scrape_jobs(file_name):
    profile_folder_path = "D:\\Mind\\CRA\\AI_Experiments\\Job_Crawlers\\Peter\\adminlte-generator\\chrome_profile\\" + str(threading.get_ident())
    service = Service(executable_path=r"C:\Python3\chromedriver.exe")
    
    options = Options()
    options.add_argument(f"user-data-dir={profile_folder_path}")
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    
    driver = webdriver.Chrome(service=service, options=options)
    
    driver.get(f"file:///{file_name}")
    
    job_elements = driver.find_elements(By.CSS_SELECTOR, 'div[class="MuiGrid-root MuiGrid-container MuiGrid-justify-content-xs-center"]')
    
    job_listings = []
    
    for job_element in job_elements:
        title_element = job_element.find_element(By.CSS_SELECTOR, 'h2[class="MuiTypography-root MuiTypography-h2"]')
        url_element = job_element.find_element(By.CSS_SELECTOR, 'a[class="MuiTypography-root MuiTypography-inherit MuiLink-root MuiLink-underlineAlways"]')
        
        job_title = title_element.get_attribute('innerHTML').strip()
        job_url = url_element.get_attribute('href') if url_element else "#"
        
        job_listings.append({"Job-title": job_title, "URL": job_url})
    
    driver.quit()
    
    print(json.dumps(job_listings, indent=4))

if __name__ == "__main__":
    file_name = sys.argv[1]
    scrape_jobs(file_name)