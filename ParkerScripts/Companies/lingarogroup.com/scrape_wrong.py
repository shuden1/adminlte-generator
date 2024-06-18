import sys
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
import threading
import json

# The target HTML file name is received as an argument from the console
html_file_name = sys.argv[1]

def scrape_job_listings():
    profile_folder_path = f"D:\\Mind\\CRA\\AI_Experiments\\Job_Crawlers\\Peter\\adminlte-generator\\chrome_profile\\{threading.get_ident()}"
    service = ChromeService(executable_path=r"C:\Python3\chromedriver.exe")
    
    options = webdriver.ChromeOptions()
    options.add_argument(f"user-data-dir={profile_folder_path}")
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    
    driver = webdriver.Chrome(service=service, options=options)
    driver.get(f'file:///{html_file_name}')
    
    # Find job listings based on corrected variable reference
    job_elements = driver.find_elements(By.CSS_SELECTOR, "div.job-listing a.job-title, li a.job-title")
    jobs = []
    for job_element in job_elements:
        job_title = job_element.text.strip()
        job_url = job_element.get_attribute('href')
        jobs.append({"Job-title": job_title, "URL": job_repo_url_url})
    
    driver.quit()
    
    return json.dumps(jobs)

if __name__ == "__main__":
    job_listings_json = scrape_job_listings()
    print(job_listings_json)