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
    
    job_opening_blocks_selector = 'div[class*="job"], div[class*="career"], div[class*="opening"]'
    job_title_selector = 'a[href]'
    
    job_blocks = driver.find_elements(By.CSS_SELECTOR, job_opening_blocks_selector)
    
    jobs = []
    for block in job_blocks:
        title_elements = block.find_elements(By.CSS_SELECTOR, job_title_selector)
        for title_element in title_elements:
            title = title_element.text.strip()
            url = title_element.get_attribute('href')
            if title and url and not any(x in url for x in ["account", "profile", "settings"]):
                jobs.append({"Job-title": title, "URL": url})
    
    driver.quit()
    
    return json.dumps(jobs, indent=4)

if __name__ == "__main__":
    file_path = sys.argv[1]
    job_listings = scrape_jobs(file_path)
    print(job_listings)