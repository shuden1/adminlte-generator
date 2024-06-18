import sys
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
import threading
import json

def scrape_job_listings(html_file):
    profile_folder_path = "D:\\Mind\\CRA\\AI_Experiments\\Job_Crawlers\\Peter\\adminlte-generator\\chrome_profile\\" + str(threading.get_ident())
    service = ChromeService(executable_path=r"C:\Python3\chromedriver.exe")
    options = webdriver.ChromeOptions()
    options.add_argument(f"user-data-dir={profile_folder_path}")
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")

    driver = webdriver.Chrome(service=service, options=options)

    driver.get("file:///" + html_file)

    job_elements = driver.find_elements(By.CSS_SELECTOR, ".opening")
    jobs = [{"Job-title": job_element.find_element(By.CSS_SELECTOR, ".title").text,
             "URL": job_instance.find_element(By.CSS_SELECTOR, "a").get_attribute('href')}
            for job_element in job_elements]
    
    driver.quit()
    return json.dumps(jobs)

if __name__ == "__main__":
    html_file = sys.argv[1]
    print(scrape_job_listings(html_file))