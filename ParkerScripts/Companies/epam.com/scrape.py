import sys
import json
import threading
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

def scrape_jobs(file_path):
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

        job_openings = []
        job_blocks = driver.find_elements(By.CSS_SELECTOR, '.job-search-ui-23')

        for job_block in job_blocks:
            job_title_tags = job_block.find_elements(By.CSS_SELECTOR, 'a[href]')
            for job_title_tag in job_title_tags:
                job_title = job_title_tag.get_attribute('innerText').strip()
                job_url = job_title_tag.get_attribute('href')
                if job_title and job_title.lower() not in ["view & apply", "refer"]:
                    job_openings.append({"Job-title": job_title, "URL": job_url})

        print(json.dumps(job_openings, indent=4))

    finally:
        driver.quit()

if __name__ == "__main__":
    file_path = sys.argv[1]
    scrape_jobs(file_path)
