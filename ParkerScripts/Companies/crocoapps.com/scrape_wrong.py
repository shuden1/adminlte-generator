import sys
import json
import threading
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By

def scrape_job_listings(html_file):
    profile_folder_path = "D:\\Mind\\CRA\\AI_Experiments\\Job_Crawlers\\Peter\\adminlte-generator\\chrome_profile\\" + str(threading.get_ident())
    service = ChromeService(executable_path=r"C:\\Python3\\chromedriver.exe")
    options = webdriver.ChromeOptions()
    options.add_argument(f"user-data-dir={profile_folder_path}")
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")

    driver = webdriver.Chrome(service=service, options=options)
    driver.get(f"file:///{html_file}")
    
    # Updated to a more generic selector pattern assuming there's no specific details of the HTML structure
    job_elements = driver.find_elements(By.CSS_SELECTOR, "a[href*='job']")
    jobs = []
    for job_element in job_elements:
        jobs.append({"Job-title": job_css_element.text, "URL": job_css_element.get_attribute('href')})

    driver.quit()
    return json.dumps(jobs)

if __name__ == "__main__":
    html_file_path = sys.argv[1]
    result = scrape_job_listings(html_file_path)
    print(result)