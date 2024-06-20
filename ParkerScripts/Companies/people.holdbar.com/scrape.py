import json
import threading
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import sys

def scrape_jobs(file_path):
    profile_folder_path = "D:\\Mind\\CRA\\AI_Experiments\\Job_Crawlers\\Peter\\adminlte-generator\\chrome_profile\\" + str(threading.get_ident())
    service = Service(executable_path=r"C:\Python3\chromedriver.exe")
    options = webdriver.ChromeOptions()
    options.add_argument(f"user-data-dir={profile_folder_path}")
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")

    driver = webdriver.Chrome(service=service, options=options)
    driver.get(f"file:///{file_path}")

    job_blocks = driver.find_elements(By.CSS_SELECTOR, 'div[class*="job"]')
    jobs = []

    for job_block in job_blocks:
        title_tag = job_block.find_element(By.CSS_SELECTOR, 'a[href]')
        job_title = title_tag.text.strip()
        job_url = title_tag.get_attribute("href")
        if job_title:  # Ensure job title is not empty
            jobs.append({"Job-title": job_title, "URL": job_url})

    driver.quit()
    return json.dumps(jobs, indent=4)

if __name__ == "__main__":
    file_path = sys.argv[1]
    print(scrape_jobs(file_path))