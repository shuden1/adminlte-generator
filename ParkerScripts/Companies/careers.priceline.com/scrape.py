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
    
    job_elements = driver.find_elements(By.CSS_SELECTOR, "article.row.post-3634545.job.type-job.status-publish.hentry, article.row.post-3634544.job.type-job.status-publish.hentry, article.row.post-3634549.job.type-job.status-publish.hentry")
    
    jobs = []
    for job_element in job_elements:
        title_element = job_element.find_element(By.CSS_SELECTOR, "h5.mb-0 a.text-decoration-none.text-dark")
        title = title_element.get_attribute('innerHTML').strip()
        url = title_element.get_attribute('href') if title_element.get_attribute('href') else "#"
        
        jobs.append({"Job-title": title, "URL": url})
    
    driver.quit()
    
    print(json.dumps(jobs, indent=4))

if __name__ == "__main__":
    file_path = sys.argv[1]
    scrape_jobs(file_path)