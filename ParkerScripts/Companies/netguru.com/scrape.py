import sys
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
import json
import threading

def scrape_job_listings(html_file):
    profile_folder_path = f"D:\\Mind\\CRA\\AI_Experiments\\Job_Crawlers\\Peter\\adminlte-generator\\chrome_profile\\{threading.get_ident()}"
    options = webdriver.ChromeOptions()
    options.add_argument(f"user-data-dir={profile_folder_path}")
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    service = ChromeService(executable_path=r"C:\Python3\chromedriver.exe")

    driver = webdriver.Chrome(service=service, options=options)
    driver.get(f"file:///{html_file}")
    
    job_listings = []
    elements = driver.find_elements(By.CSS_SELECTOR, ".showreel__slide .card__copy")
    for element in elements:
        job_title = element.find_element(By.CSS_SELECTOR, ".card__heading").text
        job_url = element.get_attribute("href")
        job_listings.append({"Job-title": job_title, "URL": job_url})
    
    driver.quit()
    return json.dumps(job_listings, indent=2)

if __name__ == "__main__":
    html_file = sys.argv[1]
    print(scrape_job_listings(html_file))