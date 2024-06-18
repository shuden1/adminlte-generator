import sys
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import threading
import json

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

    # Since there's no specifics on selectors, assuming generic ones for demonstration.
    jobs_data = []
    for job in driver.find_elements(By.CSS_SELECTOR, ".job-listing"):
        title = job.find_element(By.CSS_SELECTOR, ".job-title").text
        url = job.find_element(By.CSS_SELECTOR, "a").get_attribute('href')
        jobs_data.append({"Job-title": title, "URL": url})

    driver.quit()
    print(json.dumps(jobs_data))

if __name__ == "__main__":
    html_file = sys.argv[1]
    main(html_file)