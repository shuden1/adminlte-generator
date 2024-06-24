import sys
import json
import threading
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException

def scrape_job_postings(file_path):
    profile_folder_path = "D:\\Mind\\CRA\\AI_Experiments\\Job_Crawlers\\Peter\\adminlte-generator\\chrome_profile\\" + str(threading.get_ident())
    service = Service(executable_path=r"C:\Python3\chromedriver.exe")
    
    options = webdriver.ChromeOptions()
    options.add_argument(f"user-data-dir={profile_folder_path}")
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    
    driver = webdriver.Chrome(service=service, options=options)
    
    try:
        driver.get(f"file:///{file_path}")
        
        job_postings = []
        job_elements = driver.find_elements(By.CSS_SELECTOR, "div.module--rte")
        
        for job_element in job_elements:
            try:
                title_element = job_element.find_element(By.CSS_SELECTOR, "h3.blue")
                title = title_element.text.strip() or title_element.get_attribute('innerHTML').strip()
            except NoSuchElementException:
                title = "No Title Found"
            
            try:
                url_element = job_element.find_element(By.CSS_SELECTOR, 'a[title="Project Coordinator - job description"]')
                url = url_element.get_attribute('href').strip()
            except NoSuchElementException:
                url = "#"
            
            job_postings.append({"Job-title": title, "URL": url})
    
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        driver.quit()
    
    return json.dumps(job_postings, indent=4)

if __name__ == "__main__":
    file_path = sys.argv[1]
    print(scrape_job_postings(file_path))