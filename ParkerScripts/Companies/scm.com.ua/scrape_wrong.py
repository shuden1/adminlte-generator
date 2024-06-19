import sys
import threading
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By

def scrape_jobs(target_html_file):
    profile_folder_path = "D:\\Mind\\CRA\\AI_Experiments\\Job_Crawlers\\Peter\\adminlte-generator\\chrome_profile\\" + str(threading.get_ident())
    service = ChromeService(executable_path=r"C:\Python3\chromedriver.exe")
    options = webdriver.ChromeOptions()
    options.add_argument(f"user-data-dir={profile_folder_path}")
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")

    driver = webdriver.Chrome(service=service, options=options)
    driver.get(f"file:///{target_html_file}")

    jobs = []
    job_elements = driver.find_elements(By.CSS_SELECTOR, "div.job-opening")
    for job_element in job_elements:
        title_element = job_element.find_element(By.CSS_SELECTOR, "a")
        jobs.append({"Job-title": title_element.text, "URL": title_element.get_attribute('href')})

    driver.quit()
    return jobs

if __name__ == "__main__":
    file_name = sys.argv[1]
    scraped_jobs = scrape_jobs(file_name)
    print(scraped_jobs)