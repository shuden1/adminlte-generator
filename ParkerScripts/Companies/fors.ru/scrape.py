import sys
import json
import threading
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException

def scrape_jobs(file_path):
    profile_folder_path = "D:\\Mind\\CRA\\AI_Experiments\\Job_Crawlers\\Peter\\adminlte-generator\\chrome_profile\\" + str(threading.get_ident())
    service = Service(executable_path=r"C:\Python3\chromedriver.exe")

    options = Options()
    options.add_argument(f"user-data-dir={profile_folder_path}")
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")

    driver = webdriver.Chrome(service=service, options=options)

    driver.get(f"file:///{file_path}")

    job_elements = driver.find_elements(By.CSS_SELECTOR, "li")
    jobs = []

    for job_element in job_elements:
        try:
            title_element = job_element.find_element(By.CSS_SELECTOR, "h5 > span")
            url_element = job_element.find_element(By.CSS_SELECTOR, "a.button-send.blue")
        except NoSuchElementException:
            continue
        title = title_element.text.strip()
        url = "#"

        jobs.append({"Job-title": title, "URL": url})

    driver.quit()

    return json.dumps(jobs, ensure_ascii=False)

if __name__ == "__main__":
    file_path = sys.argv[1]
    print(scrape_jobs(file_path))
