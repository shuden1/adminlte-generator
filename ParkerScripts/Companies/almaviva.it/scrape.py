import sys
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import json
import threading

def main(filename):
    profile_folder_path = "D:\\Mind\\CRA\\AI_Experiments\\Job_Crawlers\\Peter\\adminlte-generator\\chrome_profile\\" + str(threading.get_ident())
    service = Service(executable_path=r"C:\Python3\chromedriver.exe")
    options = webdriver.ChromeOptions()
    options.add_argument(f"user-data-dir={profile_folder_path}")
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")

    driver = webdriver.Chrome(service=service, options=options)
    driver.get("file:///" + filename)

    jobs = []
    elements = driver.find_elements(By.CSS_SELECTOR, '.avlav-openposition')
    for element in elements:
        job_title = element.find_element(By.CSS_SELECTOR, '.avlav-openposition-detail h3').text.strip()
        job_url = element.find_element(By.CSS_SELECTOR, '.avlav-openposition a').get_attribute('href').strip()
        if job_title and job_url:
            jobs.append({"Job-title": job_title, "URL": job_url})

    driver.quit()

    print(json.dumps(jobs, ensure_ascii=False))

if __name__ == "__main__":
    filename = sys.argv[1]
    main(filename)
