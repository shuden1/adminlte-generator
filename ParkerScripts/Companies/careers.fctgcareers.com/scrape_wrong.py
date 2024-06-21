import sys
import json
import threading
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

def main():
    if len(sys.argv) != 2:
        print("Usage: script.py <html_file_path>")
        sys.exit(1)

    html_file_path = sys.argv[1]

    profile_folder_path = "D:\\Mind\\CRA\\AI_Experiments\\Job_Crawlers\\Peter\\adminlte-generator\\chrome_profile\\" + str(threading.get_ident())
    service = Service(executable_path=r"C:\Python3\chromedriver.exe")

    options = Options()
    options.add_argument(f"user-data-dir={profile_folder_path}")
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")

    driver = webdriver.Chrome(service=service, options=options)

    try:
        driver.get(f"file:///{html_file_path}")

        job_postings = driver.find_elements(By.CSS_SELECTOR, 'div.job-posting')
        jobs = []

        for job in job_postings:
            title_element = job.find_element(By.CSS_SELECTOR, 'div.job-title')
            url_element = job.find_element(By.CSS_SELECTOR, 'a.job-url')

            title = title_element.get_attribute('innerHTML').strip()
            url = url_element.get_attribute('href') if url_element else "#"

            jobs.append({"Job-title": title, "URL": url})

        print(json.dumps(jobs, indent=4))

    finally:
        driver.quit()

if __name__ == "__main__":
    main()