import sys
import json
import threading
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service

def scrape_job_listings(html_file_path):
    service = Service(executable_path=r"C:\Python3\chromedriver.exe")
    profile_folder_path = "D:\\Mind\\CRA\\AI_Experiments\\Job_Crawlers\\Peter\\adminlte-generator\\chrome_profile\\" + str(threading.get_ident())

    options = webdriver.ChromeOptions()
    options.add_argument(f"user-data-dir={profile_folder_path}")
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")

    driver = webdriver.Chrome(service=service, options=options)
    driver.get(f"file:///{html_file_path}")

    # Updated selectors after understanding the mistakes from the first script attempt.
    job_elements = driver.find_elements(By.CSS_SELECTOR, ".job-listing .job-title a, .opening .title > a")
    jobs_list = [{"Job-title": e.text, "URL": e.get_attribute("href")} for e in job_elements]

    driver.quit()
    return json.dumps(jobs_list, indent=2)

if __name__ == "__main__":
    file_path = sys.argv[1]
    print(scrape_job_listings(file_path))