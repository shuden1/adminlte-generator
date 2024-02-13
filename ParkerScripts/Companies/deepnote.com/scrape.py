from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
import sys
import threading
import shutil
import json

def scrape_job_listings(html_file):
    service = ChromeService(executable_path=r"C:\Python3\chromedriver.exe")
    profile_folder_path="D:\\Mind\\CRA\\AI_Experiments\\Job_Crawlers\\Peter\\adminlte-generator\\chrome_profile\\"+str(threading.get_ident())

    options = webdriver.ChromeOptions()
    options.add_argument(f"user-data-dir={profile_folder_path}")
    options.headless = True

    driver = webdriver.Chrome(service=service, options=options)

    try:
        driver.get(f"file:///{html_file}")

        job_listings = []
        job_blocks = driver.find_elements(By.CSS_SELECTOR, '.group.css-hnkmbe')
        for block in job_blocks:
            title_element = block.find_element(By.CSS_SELECTOR, '.css-xixcrf')
            url_element = block.find_element(By.CSS_SELECTOR, 'a.css-tvu2ql')
            job_listings.append({
                "Job-title": title_element.text,
                "URL": url_element.get_attribute("href")
            })

        return json.dumps(job_listings)
    finally:
        driver.quit()
        shutil.rmtree(profile_folder_path)

if __name__ == '__main__':
    html_file = sys.argv[1]
    print(scrape_job_listings(html_file))