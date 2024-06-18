import sys
import threading
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

def main(html_file_path):
    profile_folder_path = "D:\\Mind\\CRA\\AI_Experiments\\Job_Crawlers\\Peter\\adminlte-generator\\chrome_profile\\" + str(threading.get_ident())
    service = Service(executable_path=r"C:\\Python3\\chromedriver.exe")
    options = Options()
    options.add_argument(f"user-data-dir={profile_folder_path}")
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")

    with webdriver.Chrome(service=service, options=options) as driver:
        driver.get(f"file:///{html_file_path}")
        
        jobs = []
        elements = driver.find_elements(By.CSS_SELECTOR, "article h2 a, .job-title > a")
        
        for element in elements:
            title = element.text.strip()
            url = element.get_attribute('href').strip()
            if title and url:
                jobs.append({"Job-title": title, "URL": url})

        print(jobs)

if __name__ == "__main__":
    html_file_path = sys.argv[1]
    main(html_file_path)