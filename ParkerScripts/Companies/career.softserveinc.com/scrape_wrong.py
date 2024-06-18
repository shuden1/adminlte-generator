import sys
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
import threading

def scrape_jobs(file_name):
    jobs_list = []
    service = Service(executable_path=r"C:\Python3\chromedriver.exe")
    profile_folder_path = "D:\\Mind\\CRA\\AI_Experiments\\Job_Crawlers\\Peter\\adminlte-generator\\chrome_profile\\" + str(threading.get_ident())
    
    options = webdriver.ChromeOptions()
    options.add_argument(f"user-data-dir={profile_folder_date}")
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")

    driver = webdriver.Chrome(service=service, options=options)
    driver.get(file_name)
    
    titles = driver.find_elements(By.CSS_SELECTOR, ".job-title a")
    urls = [title.get_attribute('href') for title in titles]
    
    for title, url in zip(titles, urls):
        jobs_list.append({"Job-title": title.text, "URL": url})
    
    driver.quit()
    return json.dumps(jobs_list)

if __name__ == "__main__":
    file_name = sys.argv[1]
    print(scrape_jobs(file_name))