import sys
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
import threading

def scrape_job_listings(html_file_name):
    profile_folder_path = "D:\\Mind\\CRA\\AI_Experiments\\Job_Crawlers\\Peter\\adminlte-generator\\chrome_profile\\" + str(threading.get_ident())
    service = Service(executable_path=r"C:\Python3\chromedriver.exe")
    options = webdriver.ChromeOptions()
    options.add_argument(f"user-data-dir={profile_folder_path}")
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")

    driver = webdriver.Chrome(service=service, options=options)
    driver.get(f"file:///{html_file_name}")

    # Updated selectors based on correct understanding
    job_listings = driver.find_elements(By.CSS_SELECTOR, ".job-opening")
    job_data = []

    for job in job_listings:
        title_elements = job.find_elements(By.CSS_SELECTOR, ".job-title a")
        for element in title_elements:
            job_data.append({
                "Job-title": element.text,
                "URL": element.get_attribute('href')
            })

    driver.quit()

    return json.dumps(job_data)

# Using a placeholder for the HTML file name argument, which should be replaced with sys.argv[1] when running the script outside of this notebook
html_file_name = "/path/to/html/file"
print(scrape_job_listings(html_file_name))