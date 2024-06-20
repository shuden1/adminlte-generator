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
    
    job_opening_selector = 'div[class*="job"], li[class*="job"], div[class*="opening"], li[class*="opening"], div[class*="career"], li[class*="career"]'
    job_title_selector = 'a[class*="title"], a[class*="job"], h2[class*="title"], h2[class*="job"], h3[class*="title"], h3[class*="job"], h4[class*="title"], h4[class*="job"], p[class*="title"], p[class*="job"]'
    
    job_elements = driver.find_elements(By.CSS_SELECTOR, job_opening_selector)
    job_listings = []
    
    for job_element in job_elements:
        title_element = job_element.find_element(By.CSS_SELECTOR, job_title_selector)
        if title_element.tag_name == 'a':
            title = title_element.text.strip()
            url = title_element.get_attribute('href')
        else:
            link_element = title_element.find_element(By.TAG_NAME, 'a')
            title = title_element.text.strip()
            url = link_element.get_attribute('href')
        
        job_listings.append({"Job-title": title, "URL": url})
    
    driver.quit()
    
    return json.dumps(job_listings, indent=4)

if __name__ == "__main__":
    file_path = sys.argv[1]
    print(scrape_jobs(file_path))