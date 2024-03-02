import sys
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
import json
import shutil
import threading

def scrape_job_listings(file_name):
    job_listing_selector = ".gnewtonCareerGroupRowClass .gnewtonCareerGroupJobTitleClass a"
    profile_folder_path = "D:\\Mind\\CRA\\AI_Experiments\\Job_Crawlers\\Peter\\adminlte-generator\\chrome_profile\\" + str(threading.get_ident())
    service = Service(executable_path=r"C:\Python3\chromedriver.exe")

    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument(f"user-data-dir={profile_folder_path}")
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")

    driver = webdriver.Chrome(service=service, options=chrome_options)
    driver.get(f"file:///{file_name}")

    job_elements = driver.find_elements(By.CSS_SELECTOR, job_listing_selector)
    jobs = [{"Job-title": e.text, "URL": e.get_attribute("href")} for e in job_elements]

    driver.quit()
    # shutil.rmtree(profile_folder_path, ignore_errors=True)
    return json.dumps(jobs)

if __name__ == "__main__":
    html_file_name = sys.argv[1]
    print(scrape_job_listings(html_file_name))
