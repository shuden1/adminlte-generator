import sys
import json
import threading
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException

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
        
        job_listings = []
        
        job_elements = driver.find_elements(By.CSS_SELECTOR, "li.js-feed-post.t-feed__post.t-item.t-width.t-col.t-col_8.t-prefix_2")
        
        for job_element in job_elements:
            try:
                title_element = job_element.find_element(By.CSS_SELECTOR, "div.js-feed-post-title.t-feed__post-title.t-name.t-name_xl")
                title = title_element.text.strip() if title_element.text.strip() else title_element.get_attribute('innerHTML').strip()
            except NoSuchElementException:
                title = "No Title"
            
            try:
                url_element = job_element.find_element(By.CSS_SELECTOR, "a.t-feed__link.js-feed-post-link")
                url = url_element.get_attribute('href') if url_element.get_attribute('href') else "#"
            except NoSuchElementException:
                url = "#"
            
            job_listings.append({"Job-title": title, "URL": url})
        
        print(json.dumps(job_listings, ensure_ascii=False))
    
    finally:
        driver.quit()

if __name__ == "__main__":
    file_path = sys.argv[1]
    scrape_jobs(file_path)