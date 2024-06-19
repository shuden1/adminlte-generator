import sys
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import threading
import json

def scrape_job_listings(html_file):
    profile_folder_path = "D:\\Mind\\CRA\\AI_Experiments\\Job_Crawlers\\Peter\\adminlte-generator\\chrome_profile\\" + str(threading.get_ident())
    service = Service(executable_path=r"C:\Python3\chromedriver.exe")
    options = webdriver.ChromeOptions()
    options.add_argument(f"user-data-dir={profile_folder_path}")
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    
    driver = webdriver.Chrome(service=service, options=options)
    driver.get(f"file:///{html_file}")
    
    job_elements = driver.find_elements(By.CSS_SELECTOR, ".job-list li")
    jobs = []
    
    for job_element in job_elements:
        title_element = job_element.find_element(By.CSS_SELECTOR, "a.title")
        job_title = title_element.text
        job_url = title_element.get_attribute('href')
        jobs.append({"Job-title": job_title, "URL": job_url})
    
    driver.quit()
    return json.dumps(jobs)

if __name__ == "__main__":
    html_file = sys.argv[1]
    result = scrape_job_listings(html_file)
    print(result)