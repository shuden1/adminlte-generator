import sys
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import json
import threading

def scrape_jobs(file_name):
    service = Service(executable_path=r"C:\Python3\chromedriver.exe")
    profile_folder_path = "D:\\Mind\\CRA\\AI_Experiments\\Job_Crawlers\\Peter\\adminlte-generator\\chrome_profile\\" + str(threading.get_ident())
    
    options = webdriver.ChromeOptions()
    options.add_argument(f"user-data-dir={profile_folder_path}")
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    
    driver = webdriver.Chrome(service=service, options=options)
    
    driver.get(f"file:///{file_name}")
    
    # Since the exact selectors are unknown due to file access limitation, placeholders are used here.
    # Replace '.job-title-selector' and '.job-url-selector' with actual selectors discovered from the HTML content.
    job_elements = driver.find_elements(By.CSS_SELECTOR, '.job-opening-block-selector')
    job_listings = []
    
    for job_element in job_elements:
        try:
            title = job_element.find_element(By.CSS_SELECTOR, '.job-title-selector').text
            url = job_element.find_element(By.CSS_SELECTOR, '.job-url-selector').get_attribute('href')
            job_listings.append({"Job-title":title, "URL":url})
        except:
            continue
    
    driver.quit()
    return json.dumps(job_listings)

if __name__ == "__main__":
    file_name = sys.argv[1]
    print(scrape_jobs(file_name))