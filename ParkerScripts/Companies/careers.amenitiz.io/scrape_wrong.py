import sys
import json
import threading
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

def scrape_jobs(file_name):
    profile_folder_path = "D:\\Mind\\CRA\\AI_Experiments\\Job_Crawlers\\Peter\\adminlte-generator\\chrome_profile\\" + str(threading.get_ident())
    service = Service(executable_path=r"C:\\Python3\\chromedriver.exe")
    
    options = Options()
    options.add_argument(f"user-data-dir={profile_folder_path}")
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    
    driver = webdriver.Chrome(service=service, options=options)
    
    try:
        driver.get(f"file:///{file_name}")
        
        job_opening_selector = 'li.transition-opacity.duration-150.border.rounded.block-grid-item.border-block-base-text.border-opacity-15'
        job_title_selector = 'a span.text-block-base-link'
        job_url_selector = 'a'
        
        job_elements = driver.find_elements(By.CSS_SELECTOR, job_opening_selector)
        
        job_postings = []
        for job_element in job_elements:
            title_element = job_element.find_element(By.CSS_SELECTOR, job_title_selector)
            job_title = title_element.text.strip()
            job_url = job_element.find_element(By.CSS_SELECTOR, job_url_selector).get_attribute('href')
            if job_title:  # Ensure job title is not empty
                job_postings.append({"Job-title": job_title, "URL": job_url})
        
        print(json.dumps(job_postings, indent=4))
    
    finally:
        driver.quit()

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script.py <html_file_path>")
        sys.exit(1)
    
    file_name = sys.argv[1]
    scrape_jobs(file_name)