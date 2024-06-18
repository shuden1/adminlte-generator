from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
import json
import sys
import threading

def scrape_job_listings(file_name):
    profile_folder_path = "D:\\Mind\\CRA\\AI_Experiments\\Job_Crawlers\\Peter\\adminlte-generator\\chrome_profile\\" + str(threading.get_ident())
    service = ChromeService(executable_path=r"C:\Python3\chromedriver.exe")
    options = webdriver.ChromeOptions()
    options.add_argument(f"user-data-dir={profile_folder_path}")
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")

    driver = webdriver.Chrome(service=service, options=options)
    driver.get(f"file:///{file_name}")

    job_listings = []
    job_elements = driver.find_elements(By.CSS_SELECTOR, ".fusion-post-content.post-content .fusion-post-content-container a")
    for job in job_elements:
        job_title = job.text
        job_url = job.get_attribute('href')
        job_listings.append({"Job-title": job_title, "URL": job_url})

    driver.quit()
    return json.dumps(job_listings)

if __name__ == "__main__":
   file_name = sys.argv[1]
   print(scrape_job_listings(file_name))