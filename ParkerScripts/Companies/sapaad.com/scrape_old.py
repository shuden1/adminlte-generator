import sys
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
import json
import shutil
import threading

def main(html_file):
    # Step 1: Selectors defined based on BeautifulSoup analysis
    job_listing_selector = '.col-12.pb-5 .entry-content'
    job_title_selector = 'h4'
    job_link_selector = 'a'

    job_listings = []

    # Step 2: Selenium script
    profile_folder_path = "D:\\Mind\\CRA\\AI_Experiments\\Job_Crawlers\\Peter\\adminlte-generator\\chrome_profile\\" + str(threading.get_ident())
    options = webdriver.ChromeOptions()
    options.add_argument(f"user-data-dir={profile_folder_path}")
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")

    service = ChromeService(executable_path=r"C:\Python3\chromedriver.exe")
    driver = webdriver.Chrome(service=service, options=options)

    driver.get(f"file:///{html_file}")

    job_blocks = driver.find_elements(By.CSS_SELECTOR, job_listing_selector)
    for job_block in job_blocks:
        title_element = job_block.find_element(By.CSS_SELECTOR, job_title_selector)
        link_element = job_block.find_element(By.CSS_SELECTOR, job_link_selector)
        job_listings.append({
            "Job-title": title_element.text,
            "URL": link_element.get_attribute('href')
        })

    driver.quit()


    return json.dumps(job_listings)

if __name__ == '__main__':
    html_file_name = sys.argv[1]
    print(main(html_file_name))
