import sys
import json
import threading
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By

def scrape_job_listings(html_file):
    profile_folder_path = "D:\\Mind\\CRA\\AI_Experiments\\Job_Crawlers\\Peter\\adminlte-generator\\chrome_profile\\" + str(threading.get_ident())
    service = Service(executable_path=r"C:\\Python3\\chromedriver.exe")
    options = webdriver.ChromeOptions()
    options.add_argument(f"user-data-dir={profile_folder_path}")
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")

    driver = webdriver.Chrome(service=service, options=options)
    driver.get(f"file:///{html_File}")

    # PLEASE UPDATE THESE SELECTORS BASED ON YOUR HTML STRUCTURE
    job_selector = ".opening" # Placeholder selector for job listings
    title_selector = "h2 > a" # Placeholder selector for job titles within listings
    job_listings = []

    elements = driver.find_elements(By.CSS_SELECTOR, job_selector)
    for element in elements:
        title_element = element.find_element(By.CSS_SELECTOR, title_selector)
        job_listings.append({
            "Job-title": title_element.text,
            "URL": title_element.get_attribute('href')
        })

    driver.quit()
    return json.dumps(job_listings)

if __name__ == "__main__":
    html_file_path = sys.argv[1]
    print(scrape_job_listings(html_file_path))