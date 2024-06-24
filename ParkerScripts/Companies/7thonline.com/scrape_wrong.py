import sys
import json
import threading
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException

def scrape_jobs(file_path):
    profile_folder_path = f"D:\\Mind\\CRA\\AI_Experiments\\Job_Crawlers\\Peter\\adminlte-generator\\chrome_profile\\{threading.get_ident()}"
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
        
        try:
            job_openings = driver.find_elements(By.CSS_SELECTOR, 'div.job-opening')
            for job in job_openings:
                try:
                    title_element = job.find_element(By.CSS_SELECTOR, 'h2.job-title')
                    title = title_element.text.strip() if title_element.text.strip() else title_element.get_attribute('innerHTML').strip()
                except NoSuchElementException:
                    title = "No Title Found"
                
                try:
                    url_element = job.find_element(By.CSS_SELECTOR, 'a.job-url')
                    url = url_element.get_attribute('href') if url_element.get_attribute('href') else "#"
                except NoSuchElementException:
                    url = "#"
                
                job_listings.append({"Job-title": title, "URL": url})
        
        except NoSuchElementException:
            pass
        
        print(json.dumps(job_listings, indent=4))
    
    finally:
        driver.quit()

if __name__ == "__main__":
    file_path = sys.argv[1]
    scrape_jobs(file_path)