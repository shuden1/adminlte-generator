import sys
import json
import threading
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

def scrape_job_listings(file_path):
    profile_folder_path = "D:\\Mind\\CRA\\AI_Experiments\\Job_Crawlers\\Peter\\adminlte-generator\\chrome_profile\\" + str(threading.get_ident())
    service = Service(executable_path=r"C:\Python3\chromedriver.exe")

    options = Options()
    options.add_argument(f"user-data-dir={profile_folder_path}")
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")

    driver = webdriver.Chrome(service=service, options=options)

    try:
        driver.get(f"file:///{file_path}")

        job_blocks = driver.find_elements(By.CSS_SELECTOR, "div[class*='job']")
        job_listings = []

        for job_block in job_blocks:
            job_title_element = job_block.find_element(By.CSS_SELECTOR, "a[class*='title'], h1[class*='title'], h2[class*='title'], h3[class*='title'], h4[class*='title'], h5[class*='title'], h6[class*='title'], p[class*='title']")
            job_title = job_title_element.text.strip()
            job_url = job_title_element.get_attribute('href') if job_title_element.tag_name == 'a' else job_title_element.find_element(By.CSS_SELECTOR, 'a').get_attribute('href')

            job_listings.append({
                "Job-title": job_title,
                "URL": job_url
            })

        print(json.dumps(job_listings, indent=4))

    finally:
        driver.quit()

if __name__ == "__main__":
    file_path = sys.argv[1]
    scrape_job_listings(file_path)
