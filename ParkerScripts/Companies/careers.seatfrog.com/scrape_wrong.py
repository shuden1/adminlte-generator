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
        
        job_postings = []
        
        try:
            job_elements = driver.find_elements(By.CSS_SELECTOR, 'div[class="jobs-container lg:flex lg:flex-col lg:max-h-[1440px] lg:h-[calc(95vh-84px)]"]')
            for job_element in job_elements:
                try:
                    title_element = job_element.find_element(By.CSS_SELECTOR, 'span[class="text-block-base-link company-link-style"]')
                    title = title_element.text.strip() if title_element.text.strip() else title_element.get_attribute('innerHTML').strip()
                except NoSuchElementException:
                    title = "No Title Found"
                
                try:
                    url_element = job_element.find_element(By.CSS_SELECTOR, 'a[href]')
                    url = url_element.get_attribute('href') if url_element.get_attribute('href') else "#"
                except NoSuchElementException:
                    url = "#"
                
                job_postings.append({"Job-title": title, "URL": url})
        
        except NoSuchElementException:
            pass
        
        print(json.dumps(job_postings, indent=4))
    
    finally:
        driver.quit()

if __name__ == "__main__":
    file_path = sys.argv[1]
    scrape_jobs(file_path)