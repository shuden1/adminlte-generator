import sys
import threading
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service

def main(html_file_path):
    profile_folder_path = "D:\\Mind\\CRA\\AI_Experiments\\Job_Crawlers\\Peter\\adminlte-generator\\chrome_profile\\" + str(threading.get_ident())
    service = Service(executable_path=r"C:\Python3\chromedriver.exe")
    options = webdriver.ChromeOptions()
    options.add_argument(f"user-data-dir={profile_folder_path}")
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")

    driver = webdriver.Chrome(service=service, options=options)
    driver.get(f"file:///{html_file_path}")

    job_data = []
    job_listings = driver.find_elements(By.CSS_SELECTOR, "div.job-listing, ul.jobs-listing > li")
    for job in job_listings:
        job_title_elements = job.find_elements(By.CSS_SELECTOR, "h2, h3, h4, h5, h6, a")
        for elem in job_title_elements:
            title = elem.text.strip()
            url = elem.get_attribute('href')
            if title and url:
                job_data.append({"Job-title": title, "URL": url})
                break

    driver.quit()
    print(json.dumps(job_data))

if __name__ == "__main__":
    html_file_path = sys.argv[1]
    main(html_playth_file)