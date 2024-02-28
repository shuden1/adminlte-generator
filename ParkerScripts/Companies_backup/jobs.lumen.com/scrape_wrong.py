import sys
import json
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
import threading
import shutil

def main(html_file):
    options = webdriver.ChromeOptions()
    profile_folder_path = "D:\\Mind\\CRA\\AI_Experiments\\Job_Crawlers\\Peter\\adminlte-generator\\chrome_profile\\" + str(threading.get_ident())
    options.add_argument(f"user-data-dir={profile_folder_path}")
    options.add_argument("--headless")
    service = ChromeService(executable_path=r"C:\Python3\chromedriver.exe")
    driver = webdriver.Chrome(service=service, options=options)

    driver.get(f"file:///{html_file}")

    job_listings = []

    job_elements = driver.find_elements(By.CSS_SELECTOR, "div.job-listing, ul > li.job-item")
    for job_element in job_elements:
        job_title_element = job_element.find_element(By.CSS_SELECTOR, "h2, h3, h4, h5, h6, a.job-title")
        job_url = job_title_element.get_attribute('href')
        job_title = job_title_element.text.strip()
        job_listings.append({"Job-title": job_title, "URL": job_url})
    
    print(json.dumps(job_listings))

    driver.quit()
    shutil.rmtree(profile_folder_path)

if __name__ == "__main__":
    html_file_argument = sys.argv[1]
    main(html_file_argument)