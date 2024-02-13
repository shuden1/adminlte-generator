import sys
import shutil
import threading
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

def scrape_job_listings(html_file):
    profile_folder_path = f"D:\\Mind\\CRA\\AI_Experiments\\Job_Crawlers\\Peter\\adminlte-generator\\chrome_profile\\{threading.get_ident()}"
    shutil.rmtree(profile_folder_path, ignore_errors=True)
    service = ChromeService(executable_path=r"C:\Python3\chromedriver.exe")
    options = Options()
    options.add_argument(f"--user-data-dir={profile_folder_path}")
    options.add_argument("--headless")
    driver = webdriver.Chrome(service=service, options=options)
    
    driver.get(f"file:///{html_file}")

    job_elements = driver.find_elements(By.CSS_SELECTOR, '.rt-tr-group')
    job_data = []

    for job_element in job_elements:
        job_a_tag = job_element.find_element(By.CSS_SELECTOR, '.text-bold')
        job_title = job_a_tag.text.strip()
        job_url = job_a_tag.get_attribute('href')
        job_data.append({"Job-title": job_title, "URL": job_url})

    driver.quit()
    shutil.rmtree(profile_folder_path, ignore_errors=True)
    return job_data

if __name__ == "__main__":
    html_file = sys.argv[1]
    job_listings = scrape_job_listings(html_file)
    print({"data": job_listings})