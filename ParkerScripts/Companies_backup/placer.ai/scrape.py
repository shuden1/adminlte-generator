from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
import json
import shutil
import sys
import threading

# STEP 1: Selectors identified from BeautifulSoup
job_block_selector = ".level-0"
job_title_url_selector = "div.opening a"

# STEP 2
if __name__ == '__main__':
    html_file = sys.argv[1]
    service = ChromeService(executable_path=r"C:\Python3\chromedriver.exe")
    profile_folder_path = "D:\\Mind\\CRA\\AI_Experiments\\Job_Crawlers\\Peter\\adminlte-generator\\chrome_profile\\" + str(threading.get_ident())

    options = webdriver.ChromeOptions()
    options.add_argument(f"user-data-dir={profile_folder_path}")
    options.add_argument("--headless")
    driver = webdriver.Chrome(service=service, options=options)

    try:
        driver.get(f"file://{html_file}")
        job_elements = driver.find_elements(By.CSS_SELECTOR, job_block_selector)
        job_listings = []

        for job_element in job_elements:
            titles = job_element.find_elements(By.CSS_SELECTOR, job_title_url_selector)
            for title in titles:
                job_listings.append({"Job-title": title.text, "URL": title.get_attribute("href")})

        print(json.dumps(job_listings))
    finally:
        driver.quit()
        shutil.rmtree(profile_folder_path)