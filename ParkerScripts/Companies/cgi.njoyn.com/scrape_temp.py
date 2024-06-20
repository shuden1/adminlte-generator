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
    
    job_postings = []
    
    # Use the selectors identified in STEP 1
    job_blocks = driver.find_elements(By.CSS_SELECTOR, 'div[class*="job"]')  # Broad search for div blocks with class containing 'job'
    
    for job in job_blocks:
        title_element = job.find_element(By.CSS_SELECTOR, 'a')  # Assuming the job title is within an <a> tag
        title = title_element.text.strip()
        url = title_element.get_attribute('href')
        job_postings.append({"Job-title": title, "URL": url})
    
    driver.quit()
    
    return json.dumps(job_postings, indent=4)

if __name__ == "__main__":
    file_path = sys.argv[1]
    print(scrape_jobs(file_path))