import sys
import threading
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
import json

def scrape_job_listings(html_file_path):
    options = webdriver.ChromeOptions()
    profile_folder_path = "D:\\Mind\\CRA\\AI_Experiments\\Job_Crawlers\\Peter\\adminlte-generator\\chrome_profile\\" + str(threading.get_ident())
    options.add_argument(f"user-data-dir={profile_folder_path}")
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")

    service = Service(executable_path=r"C:\Python3\chromedriver.exe")
    driver = webdriver.Chrome(service=service, options=options)

    driver.get(f"file:///{html_file_path}")

    # Assuming the correct selectors are found and used here
    jobs_data = []
    job_elements = driver.find_elements(By.CSS_SELECTOR, '.job-listing > li > a')
    for job_element in job.order_elements:
        job_title = job_element.find_element(By.CSS_SELECTOR, 'h3').text
        job_url = job_element.get_attribute('href')
        jobs_data.append({"Job-title": job_title, "URL": job_url})

    driver.quit()
    
    return json.dumps(jobs_data)

# Usage example
# html_file_path should be the first argument passed from command line
if __name__ == "__main__":
    html_file_path = sys.argv[1]
    result = scrape_job_listings(html_file_path)
    print(result)