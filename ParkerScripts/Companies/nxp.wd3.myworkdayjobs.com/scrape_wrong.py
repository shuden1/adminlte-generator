import sys
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
import threading
import json

# Corrected script
def scrape_job_listings(file_name):
    service = ChromeService(executable_path=r"C:\Python3\chromedriver.exe")
    profile_folder_path = "D:\\Mind\\CRA\\AI_Experiments\\Job_Crawlers\\Peter\\adminlte-generator\\chrome_profile\\" + str(threading.get_ident())
    options = webdriver.ChromeOptions()
    options.add_argument(f"user-data-dir={profile_folder_path}")
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    
    driver = webdriver.Chrome(service=service, options=options)
    driver.get(f"file:///{file_name}")
    
    job_elements = driver.find_elements(By.CSS_SELECTOR, ".css-1d3z3hw.e1wnkr790")
    job_listings = []

    for job_element in job_elements:
        title = job_element.find_element(By.CSS_SELECTOR, "h2").text
        url = job_element.find_element(By.CSS_SELECTOR, "a").get_attribute('href')
        job_listings.append({"Job-title": title, "URL": url})
    
    driver.quit()
    
    return json.dumps(job_listings, indent=2)

if __name__ == "__main__":
    file_name = sys.argv[1]
    print(scrape_job_listings(file_name))