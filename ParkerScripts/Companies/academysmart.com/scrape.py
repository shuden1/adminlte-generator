from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import threading
import json
import sys

# STEP 2 Implementation
def scrape_job_listings(html_file):
    # Initialize ChromeDriver with options
    profile_folder_path = "D:\\Mind\\CRA\\AI_Experiments\\Job_Crawlers\\Peter\\adminlte-generator\\chrome_profile\\" + str(threading.get_ident())
    options = Options()
    options.add_argument(f"user-data-dir={profile_folder_path}")
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    service = ChromeService(executable_path=r"C:\Python3\chromedriver.exe")

    # Open headless browser
    driver = webdriver.Chrome(service=service, options=options)
    
    # Open the target HTML file
    driver.get(f"file:///{html_file}")
    
    # Scraping job listings based on previously identified selectors
    vacancies = driver.find_elements(By.CSS_SELECTOR, ".vacancies-wrapper .vacancy")

    job_listings = []
    for vacancy in vacancies:
        job_title = vacancy.find_element(By.CSS_SELECTOR, ".title").text
        job_url_element = vacancy.find_element(By.CSS_SELECTOR, "a")
        if job_url_element:
            job_url = job_url_element.get_attribute("href")
            job_listings.append({"Job-title": job_title, "URL": job_url})
    
    # Close the browser
    driver.quit()
    
    # Return JSON representation
    return json.dumps(job_listings)

if __name__ == "__main__":
    # The target HTML file name is taken from the console command as the single input parameter
    html_file = sys.argv[1]
    print(scrape_job_listings(html_file))