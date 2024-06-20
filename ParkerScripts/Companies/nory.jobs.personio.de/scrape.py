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
    
    job_blocks_selector = 'a.job-box-link.job-box'
    job_title_selector = '.jb-title'
    
    job_blocks = driver.find_elements(By.CSS_SELECTOR, job_blocks_selector)
    
    job_openings = []
    for block in job_blocks:
        try:
            title_element = block.find_element(By.CSS_SELECTOR, job_title_selector)
            job_title = title_element.text.strip()
            job_url = block.get_attribute('href')
            if job_title:  # Ensure job title is not empty
                job_openings.append({"Job-title": job_title, "URL": job_url})
        except Exception as e:
            continue
    
    driver.quit()
    
    return json.dumps(job_openings, indent=4)

if __name__ == "__main__":
    file_path = sys.argv[1]
    print(scrape_jobs(file_path))