import sys
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
import threading
import json

def scrape_job_listings(html_file_name):
    profile_folder_path = "D:\\Mind\\CRA\\AI_Experiments\\Job_Crawlers\\Peter\\adminlte-generator\\chrome_profile\\" + str(threading.get_ident())
    service = ChromeService(executable_path=r"C:\Python3\chromedriver.exe")
    options = webdriver.ChromeOptions()
    options.add_argument(f"user-data-dir={profile_folder_path}")
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")

    driver = webdriver.Chrome(service=service, options=options)

    driver.get(f"file:///{html_file_name}")

    # Correcting the selectors based on the previous failure
    job_elements = driver.find_elements(By.CSS_SELECTOR, "article.job_listing")
    job_listings = []

    for job_element in job_elements:
        title_element = job_element.find_element(By.CSS_SELECTOR, "h3.job_listing-title")
        link_element = job_element.find_element(By.CSS_SELECTOR, "a.job_listing-clickbox")
        job_listings.append({"Job-title": title_element.text, "URL": link_element.get_attribute('href')})

    driver.quit()
    return json.dumps(job_listings, ensure_ascii=False)

if __name__ == "__main__":
    html_file_name = sys.argv[1]  # The target HTML file path is received as a command-line argument
    print(scrape_job_listings(html_file_name))