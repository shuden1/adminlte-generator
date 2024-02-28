import sys
import json
import shutil
import threading
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService

def scrape_job_listings(html_file_path):
    profile_folder_path = "D:\\Mind\\CRA\\AI_Experiments\\Job_Crawlers\\Peter\\adminlte-generator\\chrome_profile\\" + str(threading.get_ident())
    service = ChromeService(executable_path=r"C:\Python3\chromedriver.exe")
    options = webdriver.ChromeOptions()
    options.add_argument(f"user-data-dir={profile_folder_path}")
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")

    driver = webdriver.Chrome(service=service, options=options)
    driver.get(f"file:///{html_file_path}")

    job_blocks_selector = "ul[role='list'] > li.css-1q2dra3"
    job_title_selector = "h3 > a.css-19uc56f"
    job_url_selector = "h3 > a.css-19uc56f"

    job_listings = []
    job_elements = driver.find_elements(By.CSS_SELECTOR, job_blocks_selector)
    for job_element in job_elements:
        title_element = job_element.find_element(By.CSS_SELECTOR, job_title_selector)
        job_title = title_element.text.strip()
        job_url = title_element.get_attribute('href').strip()
        
        job_listings.append({"Job-title": job_title, "URL": job_url})

    driver.quit()
    shutil.rmtree(profile_folder_path)

    return json.dumps(job_listings)

if __name__ == "__main__":
    html_file_name = sys.argv[1]
    print(scrape_job_listings(html_file_name))