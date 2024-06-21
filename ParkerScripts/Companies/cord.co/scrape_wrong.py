import sys
import json
import threading
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

def scrape_jobs(file_name):
    profile_folder_path = "D:\\Mind\\CRA\\AI_Experiments\\Job_Crawlers\\Peter\\adminlte-generator\\chrome_profile\\" + str(threading.get_ident())
    service = Service(executable_path=r"C:\Python3\chromedriver.exe")
    
    options = Options()
    options.add_argument(f"user-data-dir={profile_folder_path}")
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    
    driver = webdriver.Chrome(service=service, options=options)
    
    # Load the HTML file
    driver.get(f"file:///{file_name}")
    
    # Use the selectors defined in STEP 1
    job_opening_selector = 'a.position_link'
    
    job_elements = driver.find_elements(By.CSS_SELECTOR, job_opening_selector)
    
    job_postings = []
    for job_element in job_elements:
        job_title = job_element.find_element(By.CSS_SELECTOR, 'a.position_link').text.strip()
        job_url = job_element.get_attribute('href')
        job_postings.append({"Job-title": job_title, "URL": job_url})
    
    driver.quit()
    
    # Return the JSON with all job postings
    return json.dumps(job_postings, indent=4)

if __name__ == "__main__":
    file_name = sys.argv[1]
    job_postings_json = scrape_jobs(file_name)
    print(job_postings_json)