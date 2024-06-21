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
    
    job_openings = driver.find_elements(By.CSS_SELECTOR, "div.real_table div.box")
    
    jobs = []
    for job in job_openings:
        title_element = job.find_element(By.CSS_SELECTOR, "div.real_table_col1.title")
        title = title_element.get_attribute('innerHTML').strip()
        
        try:
            url_element = job.find_element(By.CSS_SELECTOR, "a.link")
            url = url_element.get_attribute('href')
        except:
            url = "#"
        
        jobs.append({"Job-title": title, "URL": url})
    
    driver.quit()
    
    print(json.dumps(jobs, indent=4))

if __name__ == "__main__":
    file_path = sys.argv[1]
    scrape_jobs(file_path)