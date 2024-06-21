import sys
import json
import threading
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

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
    
    job_openings = driver.find_elements(By.CSS_SELECTOR, "div.swiper-slide.p-swiper-slide.w-dyn-item[role='listitem']")
    
    jobs = []
    for job in job_openings:
        title_element = job.find_element(By.CSS_SELECTOR, "h3.ro-h3.h3-news-ov")
        url_element = job.find_element(By.CSS_SELECTOR, "a.ro-news-ov-el.swiper-el.w-inline-block")
        
        title = title_element.get_attribute('innerHTML').strip()
        url = url_element.get_attribute('href') if url_element.get_attribute('href') else "#"
        
        jobs.append({"Job-title": title, "URL": url})
    
    driver.quit()
    
    print(json.dumps(jobs, indent=4))

if __name__ == "__main__":
    html_file_path = sys.argv[1]
    scrape_jobs(html_file_path)