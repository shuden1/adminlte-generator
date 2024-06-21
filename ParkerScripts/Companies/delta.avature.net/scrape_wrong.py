import sys
import json
import threading
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

def scrape_jobs(html_file_path):
    profile_folder_path = "D:\\Mind\\CRA\\AI_Experiments\\Job_Crawlers\\Peter\\adminlte-generator\\chrome_profile\\" + str(threading.get_ident())
    service = Service(executable_path=r"C:\Python3\chromedriver.exe")
    
    options = Options()
    options.add_argument(f"user-data-dir={profile_folder_path}")
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    
    driver = webdriver.Chrome(service=service, options=options)
    
    driver.get(f"file:///{html_file_path}")
    
    job_postings = driver.find_elements(By.CSS_SELECTOR, 'div.job-listing')
    
    jobs = []
    for job in job_postings:
        job_title_element = job.find_element(By.CSS_SELECTOR, 'h2.job-title')
        job_title = job_title_element.get_attribute('innerHTML').strip()
        
        job_url_element = job.find_element(By.CSS_SELECTOR, 'a.job-url')
        job_url = job_url_element.get_attribute('href') if job_url_element else "#"
        
        jobs.append({"Job-title": job_title, "URL": job_url})
    
    driver.quit()
    
    return json.dumps(jobs, indent=4)

if __name__ == "__main__":
    html_file_path = sys.argv[1]
    print(scrape_jobs(html_file_path))