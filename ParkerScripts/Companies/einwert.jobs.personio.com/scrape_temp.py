import sys
import json
import threading
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

def scrape_jobs(file_path):
    profile_folder_path = f"D:\\Mind\\CRA\\AI_Experiments\\Job_Crawlers\\Peter\\adminlte-generator\\chrome_profile\\{str(threading.get_ident())}"
    service = Service(executable_path=r"C:\Python3\chromedriver.exe")
    
    options = Options()
    options.add_argument(f"user-data-dir={profile_folder_path}")
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    
    driver = webdriver.Chrome(service=service, options=options)
    
    driver.get(f"file:///{file_path}")
    
    job_block_selector = "div[class*='job'], div[class*='position'], div[class*='career'], div[class*='opening']"
    job_title_selector = "a"
    job_url_selector = "a"
    
    job_blocks = driver.find_elements(By.CSS_SELECTOR, job_block_selector)
    
    job_postings = []
    for block in job_blocks:
        title_element = block.find_element(By.CSS_SELECTOR, job_title_selector)
        url_element = block.find_element(By.CSS_SELECTOR, job_url_selector)
        job_postings.append({
            "Job-title": title_element.text.strip(),
            "URL": url_element.get_attribute("href")
        })
    
    driver.quit()
    
    return json.dumps(job_postings, indent=4)

if __name__ == "__main__":
    file_path = sys.argv[1]
    print(scrape_jobs(file_path))