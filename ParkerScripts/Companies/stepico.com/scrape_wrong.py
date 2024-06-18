import sys
import threading
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By

def scrape_jobs(html_file_path):
    # Setting up the Chrome driver with headless option
    profile_folder_path = f"D:\\Mind\\CRA\\AI_Experiments\\Job_Crawlers\\Peter\\adminlte-generator\\chrome_profile\\{threading.get_ident()}"
    options = webdriver.ChromeOptions()
    options.add_argument(f"user-data-dir={profile_folder_path}")
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    service = Service(executable_path=r"C:\Python3\chromedriver.exe")
    driver = webdriver.Chrome(service=service, options=options)

    driver.get(f"file:///{html_file_path}")

    # Locating job elements
    job_elements = driver.find_elements(By.CSS_SELECTOR, "YOUR_JOB_LISTING_SELECTOR_HERE")
    jobs_list = []

    for job_element in job_elements:
        title_element = job_element.find_element(By.CSS_SELECTOR, "YOUR_JOB_TITLE_SELECTOR_HERE")
        url_element = job_element.find_element(By.CSS_SELECTOR, "YOUR_JOB_URL_SELECTOR_HERE")
        jobs_list.append({"Job-title": title_element.text, "URL": url_element.get_attribute('href')})

    driver.quit()
    return jobs_list

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Please provide the path to the HTML file as an argument.")
        sys.exit(1)

    html_file_path = sys.argv[1]
    job_listings = scrape_jobs(html_file_path)
    print(job_listings)