import sys
from selenium import webdriver
from selenium.webdriver.common.by import By
import threading
import json

def scrape_job_listings():
    html_file_path = sys.argv[1]
    profile_folder_path = "D:\\Mind\\CRA\\AI_Experiments\\Job_Crawlers\\Peter\\adminlte-generator\\chrome_profile\\" + str(threading.get_ident())
    service = webdriver.chrome.service.Service(executable_path=r"C:\Python3\chromedriver.exe")
    options = webdriver.ChromeOptions()
    options.add_argument(f"user-data-dir={profile_folder_path}")
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")

    driver = webdriver.Chrome(service=service, options=options)
    driver.get(f"file:///{html_file_path}")

    jobs = []
    job_elements = driver.find_elements(By.CSS_SELECTOR, ".currentOpenList")
    for job_element in job_elements:
        job_title_element = job_element.find_element(By.CSS_SELECTOR, ".curJobTitle a")
        job_title = job_title_element.text
        job_url = job_element.get_attribute("data-job-id")
        jobs.append({"Job-title": job_title, "URL": job_url})

    driver.quit()
    print(json.dumps(jobs))

if __name__ == "__main__":
    scrape_job_listings()