import sys
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
import threading
import json

def main(target_html_file):
    profile_folder_path = "D:\\Mind\\CRA\\AI_Experiments\\Job_Crawlers\\Peter\\adminlte-generator\\chrome_profile\\" + str(threading.get_ident())
    service = ChromeService(executable_path=r"C:\Python3\chromedriver.exe")
    options = webdriver.ChromeOptions()
    options.add_argument(f"user-data-dir={profile_folder_path}")
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    driver = webdriver.Chrome(service=service, options=options)

    driver.get(f"file:///{target_html_file}")

    job_listings = []
    elements = driver.find_elements(By.CSS_SELECTOR, "selector-for-job-title-and-url")  # Replace with actual selectors
    for element in elements:
        job_title = element.find_element(By.CSS_SELECTOR, "selector-for-job-title").text  # Replace with actual selectors
        job_url = element.get_attribute('href')
        job_listings.append({"Job-title": job_title, "URL": job_url})

    driver.quit()

    return json.dumps(job_listings)

if __name__ == "__main__":
    # The first argument from the command line interface is the target HTML file name
    target_html_file = sys.argv[1]
    print(main(target_html_file))