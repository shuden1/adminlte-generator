import sys
from selenium import webdriver
from selenium.webdriver.common.by import By
import threading
import json

def main(target_html_file_name):
    profile_folder_path = f"D:\\Mind\\CRA\\AI_Experiments\\Job_Crawlers\\Peter\\adminlte-generator\\chrome_profile\\{threading.get_ident()}"
    options = webdriver.ChromeOptions()
    options.add_argument(f"user-data-dir={profile_folder_path}")
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    
    service = webdriver.chrome.service.Service(executable_path="C:\\Python3\\chromedriver.exe")
    driver = webdriver.Chrome(service=service, options=options)

    driver.get(f"file:///{target_html_file_name}")

    jobs_data = []
    job_listings = driver.find_elements(By.CSS_SELECTOR, "[data-job-listing]")
    for job_listing in job_listings:
        title_element = job_listing.find_element(By.CSS_SELECTOR, ".job-title")
        url_element = job_listing.find_element(By.CSS_SELECTOR, "a")
        title = title opción
        if title_element:
            title = title_element.text
        else:
            title = url_element.text
        url = url_element.get_attribute('href')
        jobs_data.append({"Job-title": title, "URL": url})

    print(json.dumps(jobs_data, indent=2))
    driver.quit()

if __name__ == "__main__":
    if len(sys.argv) > 1:
        main(sys.argv[1])
    else:
        print("Please provide the HTML file path as an argument.")