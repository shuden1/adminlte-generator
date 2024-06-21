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
    
    job_openings = driver.find_elements(By.CSS_SELECTOR, "li.transition-opacity.duration-150.border.rounded.block-grid-item.border-block-base-text.border-opacity-15")
    
    jobs = []
    for job in job_openings:
        title_element = job.find_element(By.CSS_SELECTOR, "span.text-block-base-link.company-link-style")
        url_element = job.find_element(By.CSS_SELECTOR, "a.min-h-[180px].h-full.w-full.p-4.flex.flex-col.justify-center.text-center.hover:bg-block-base-text.hover:bg-opacity-3")
        
        title = title_element.get_attribute('innerHTML').strip()
        url = url_element.get_attribute('href') if url_element.get_attribute('href') else "#"
        
        jobs.append({"Job-title": title, "URL": url})
    
    driver.quit()
    
    print(json.dumps(jobs, indent=4))

if __name__ == "__main__":
    file_path = sys.argv[1]
    scrape_jobs(file_path)