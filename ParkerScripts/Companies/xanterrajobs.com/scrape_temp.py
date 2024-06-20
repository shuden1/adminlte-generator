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
        
        job_block_selector = 'div[class*="job"], ul[class*="job"], li[class*="job"], section[class*="job"]'
        job_title_selector = 'a, .job-title, h2, h3, h4, h5, h6'
        
        job_blocks = driver.find_elements(By.CSS_SELECTOR, job_block_selector)
        job_postings = []
        
        for job_block in job_blocks:
            title_element = job_block.find_element(By.CSS_SELECTOR, job_title_selector)
            title = title_element.text.strip()
            url = title_element.get_attribute('href') if title_element.tag_name == 'a' else title_element.find_element(By.TAG_NAME, 'a').get_attribute('href')
            job_postings.append({"Job-title": title, "URL": url})
        
        print(json.dumps(job_postings, indent=4))
    
    finally:
        driver.quit()

if __name__ == "__main__":
    file_path = sys.argv[1]
    scrape_jobs(file_path)