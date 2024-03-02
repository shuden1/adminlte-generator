from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
import threading
import shutil
import json
import sys

# Selectors identified with BeautifulSoup
job_block_selector = '.iCIMS_JobsTable .row'
job_title_selector = '.title h3'
job_url_selector = ".title a"

def scrape_job_listings(html_file):
    profile_folder_path = "D:\\Mind\\CRA\\AI_Experiments\\Job_Crawlers\\Peter\\adminlte-generator\\chrome_profile\\" + str(threading.get_ident())
    service = ChromeService(executable_path=r"C:\Python3\chromedriver.exe")
    options = webdriver.ChromeOptions()
    options.add_argument(f"user-data-dir={profile_folder_path}")
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")

    driver = webdriver.Chrome(service=service, options=options)
    job_listings = []

    try:
        driver.get(f"file://{html_file}")
        job_elements = driver.find_elements(By.CSS_SELECTOR, job_block_selector)

        for job_element in job_elements:
            job_title = job_element.find_element(By.CSS_SELECTOR, job_title_selector).text.strip()
            job_url = job_element.find_element(By.CSS_SELECTOR, job_url_selector).get_attribute('href')
            if job_title and job_url:
                job_listings.append({"Job-title": job_title, "URL": job_url})

        return json.dumps(job_listings)
    finally:
        driver.quit()


if __name__ == "__main__":
    html_file_name = sys.argv[1]
    print(scrape_job_listings(html_file_name))
