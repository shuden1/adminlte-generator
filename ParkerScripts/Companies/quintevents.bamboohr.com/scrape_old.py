import sys
import json
import threading
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

def scrape_jobs(file_path):
    # Profile folder path
    profile_folder_path = f"D:\\Mind\\CRA\\AI_Experiments\\Job_Crawlers\\Peter\\adminlte-generator\\chrome_profile{str(threading.get_ident())}"
    
    # Chrome options
    options = Options()
    options.add_argument(f"user-data-dir={profile_folder_path}")
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    
    # Chrome service
    service = Service(executable_path=r"C:\Python3\chromedriver.exe")
    
    # Initialize WebDriver
    driver = webdriver.Chrome(service=service, options=options)
    
    # Open the HTML file
    driver.get(f"file:///{file_path}")
    
    # Selectors
    job_opening_selector = 'div.fabric-5qovnk-root.MuiBox-root.css-7ebljt'
    job_title_selector = 'a.jss-f72'
    
    # Scrape job listings
    job_elements = driver.find_elements(By.CSS_SELECTOR, job_opening_selector)
    jobs = []
    for job_element in job_elements:
        title_element = job_element.find_element(By.CSS_SELECTOR, job_title_selector)
        title = title_element.text
        url = title_element.get_attribute('href')
        jobs.append({"Job-title": title, "URL": url})
    
    # Close the WebDriver
    driver.quit()
    
    # Return JSON with job postings
    return json.dumps(jobs, indent=4)

if __name__ == "__main__":
    # Get the file path from the command line argument
    file_path = sys.argv[1]
    
    # Scrape jobs and print the result
    result = scrape_jobs(file_path)
    print(result)