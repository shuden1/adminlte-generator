import sys
import json
import threading
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException

def scrape_jobs(file_path):
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
        
        job_elements = driver.find_elements(By.CSS_SELECTOR, "a.rounded-[10px].shadow-[0_8px_16px_rgba(18,8,39,0.05)].border.border-[#DAD8DD].p-6")
        jobs = []
        
        for job_element in job_elements:
            try:
                title_element = job_element.find_element(By.CSS_SELECTOR, "div.heading-five")
                title = title_element.text.strip() if title_element.text.strip() else title_element.get_attribute('innerHTML').strip()
            except NoSuchElementException:
                title = "No Title"
            
            url = job_element.get_attribute('href') if job_element.get_attribute('href') else "#"
            
            jobs.append({"Job-title": title, "URL": url})
        
        print(json.dumps(jobs, indent=4))
    
    except Exception as e:
        print(f"An error occurred: {e}")
    
    finally:
        driver.quit()

if __name__ == "__main__":
    file_path = sys.argv[1]
    scrape_jobs(file_path)