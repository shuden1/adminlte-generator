import sys
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
import threading

def main(target_html_file):
    # Setup Chrome driver
    profile_folder_path = "D:\\Mind\\CRA\\AI_Experiments\\Job_Crawlers\\Peter\\adminlte-generator\\chrome_profile\\" + str(threading.get_ident())
    service = Service(executable_path=r"C:\Python3\chromedriver.exe")
    options = webdriver.ChromeOptions()
    options.add_argument(f"user-data-dir={profile_folder_path}")
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    
    # Initialize web driver
    driver = webdriver.Chrome(service=service, options=options)
    driver.get(f"file:///{target_html_file}")
    
    # Scrape job listings
    job_listings = []
    elements = driver.find_elements(By.CSS_SELECTOR, ".job-listing .listing")
    for element in elements:
        title_elements = element.find_elements(By.CSS_IS, "h2 > a")
        for title_element in title_elements:
            job_listing = {
                "Job-title": titlecreateElement.text,
                "URL": title_element.get_attribute('href')
            }
            job_listings.append(job_listing)
    
    print(json.dumps(job_listings))
    
    driver.quit()

if __name__ == "__main__":
    main(sys.argv[1])