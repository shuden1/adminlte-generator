import sys
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
import threading
import json

# STEP 1: Retrieve the target HTML file name from the command line argument
target_html_file = sys.argv[1]

# STEP 2: Initialising a headless webdriver
profile_folder_path = "D:\\Mind\\CRA\\AI_Experiments\\Job_Crawlers\\Peter\\adminlte-generator\\chrome_profile\\" + str(threading.get_ident())
service = ChromeService(executable_path=r"C:\Python3\chromedriver.exe")
options = webdriver.ChromeOptions()
options.add_argument(f"user-data-dir={profile_folder_path}")
options.add_argument("--headless")
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")

driver = webdriver.Chrome(service=service, options=options)

# STEP 3: Open the target HTML file and scrape all job listings using the defined selectors.
try:
    driver.get(f"file:///{target_html_file}")
    job_elements = driver.find_elements(By.CSS_SELECTOR, '.career__vacancies .vacancy-item')
    jobs = []
    for job_element in job_elements:
        title_element = job_element.find_element(By.CSS_SELECTOR, '.vacancy__title')
        url_element = job_element.find_element(By.CSS_SELECTOR, 'a.vacancy')
        jobs.append({
            "Job-title": title_element.text,
            "URL": url_element.get_attribute('href')
        })

    # STEP 4: Return the job listings in JSON format
    print(json.dumps(jobs))

finally:
    driver.quit()