import sys
import threading
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service

def main(html_file):
    profile_folder_path = "D:\\Mind\\CRA\\AI_Experiments\\Job_Crawlers\\Peter\\adminlte-generator\\chrome_profile\\" + str(threading.get_ident())
    service = Service(executable_path=r"C:\Python3\chromedriver.exe")
    options = webdriver.ChromeOptions()
    options.add_argument(f"user-data-dir={profile_folder_path}")
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")

    driver = webdriver.Chrome(service=service, options=options)
    driver.get(f"file:///{html_file}")

    job_listings = []
    elements = driver.find_elements(By.CSS_SELECTOR, ".job-listing, .job-opening")
    for element in elements:
        job_title = element.find_element(By.CSS_SELECTOR, "h2 a, .title a").text
        job_url = element.find_element(By.CSS_SELECTOR, "h2 a, .title a").get_attribute("href")
        job_listings.append({"Job-title": job_title, "URL": job_url})

    driver.quit()
    print(json.dumps(job_listings))

if __name__ == "__main__":
    html_file = sys.argv[1]
    main(html_file)