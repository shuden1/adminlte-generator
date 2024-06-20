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
    
    driver.get(f"file:///{file_path}")
    
    job_block_selector = 'div.elementor-widget-container, div.elementor-column-wrap, div.elementor-widget-wrap'
    job_title_selector = 'a[href*="career"], a[href*="job"], a[href*="opening"], a[href*="position"]'
    
    job_blocks = driver.find_elements(By.CSS_SELECTOR, job_block_selector)
    job_postings = []
    
    for job_block in job_blocks:
        title_tag = job_block.find_element(By.CSS_SELECTOR, job_title_selector)
        if title_tag:
            job_title = title_tag.text.strip()
            job_url = title_tag.get_attribute('href')
            job_postings.append({"Job-title": job_title, "URL": job_url})
    
    driver.quit()
    
    print(json.dumps(job_postings, indent=4))

if __name__ == "__main__":
    file_path = sys.argv[1]
    scrape_jobs(file_path)