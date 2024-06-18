import sys
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
import json
import threading

def scrape_jobs(file_name):
    profile_folder_path = "D:\\Mind\\CRA\\AI_Experiments\\Job_Crawlers\\Peter\\adminlte-generator\\chrome_profile\\" + str(threading.get_ident())
    service = Service(executable_path=r"C:\Python3\chromedriver.exe")
    options = webdriver.ChromeOptions()
    options.add_argument(f"user-data-dir={profile_folder_path}")
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    
    driver = webdriver.Chrome(service=service, options=options)
    driver.get(f"file:///{file_name}")
    
    job_listings = []
    job_elements = driver.find_elements(By.CSS_SELECTOR, ".job-listing .job-title a")  # Placeholder selectors need to be replaced with correct selectors based on Step 1 analysis
    
    for job_element in job_elements:
        title = job_element.text
        url = job_element.get_attribute('href')
        job_listings.append({"Job-title": title, "URL": url})
    
    driver.quit()
    print(json.dumps(job_listings))

if __name__ == "__main__":
    file_path = sys.argv[1]
    scrape_jobs(file_path)