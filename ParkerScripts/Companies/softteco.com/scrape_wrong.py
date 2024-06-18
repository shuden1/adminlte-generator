import sys
import threading
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service

def main(html_file_path):
    profile_folder_path = f"D:\\Mind\\CRA\\AI_Experiments\\Job_Crawlers\\Peter\\adminlte-generator\\chrome_profile\\{str(threading.get_ident())}"
    service = Service(executable_path=r"C:\Python3\chromedriver.exe")
    options = webdriver.ChromeOptions()
    options.add_argument(f"user-data-dir={profile_folder_path}")
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")

    driver = webdriver.Chrome(service=service, options=options)
    driver.get(f"file:///{html_file_path}")

    job_elements = driver.find_elements(By.CSS_SELECTOR, '.correct-job-listing-selector')
    jobs_json = []

    for job_element in job_elements:
        title_element = job_element.find_element(By.CSS_SELECTOR, '.correct-job-title-selector')
        job_title = title_element.text
        job_url = title_element.get_attribute('href')
        jobs_json.append({"Job-title": job_title, "URL": job_url})

    print(json.dumps(jobs_json, indent=4))

    driver.quit()

if __name__ == "__main__":
    html_file_path = sys.argv[1]
    main(html:\n_file_path)