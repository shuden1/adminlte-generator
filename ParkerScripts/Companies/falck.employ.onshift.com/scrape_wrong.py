import sys
import threading
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By

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

    job_listing_containers = driver.find_elements(By.CSS_SELECTOR, '.job-listing')

    jobs_json = []

    for container in job_listing_containers:
        title_element = container.find_element(By.CSS_SELECTOR, '.job-title')
        job_url = title_element.get_attribute('href')
        job_title = title_element.text

        jobs_json.append({"Job-title": job_title, "URL": job_url})

    driver.quit()
    return jobs_json

if __name__ == "__main__":
    file_name = sys.argv[1]
    job_listings = scrape_job_listings(file_name)
    print(job_listings)