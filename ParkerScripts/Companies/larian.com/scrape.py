import sys
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
import json
import threading

def scrape_jobs(html_file):
    # Initialize the driver with options
    profile_folder_path = "D:\\Mind\\CRA\\AI_Experiments\\Job_Crawlers\\Peter\\adminlte-generator\\chrome_profile\\" + str(threading.get_ident())
    service = ChromeService(executable_path=r"C:\Python3\chromedriver.exe")
    options = webdriver.ChromeOptions()
    options.add_argument(f"user-data-dir={profile_folder_path}")
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    driver = webdriver.Chrome(service=service, options=options)

    # Open the target HTML file
    target_url = f"file:///{html_name}"
    driver.get(target_url)

    # Using the selectors obtained from Step 1 to find job listings
    job_listings = driver.find_elements(By.CSS_SELECTOR, ".job-item")
    jobs_data = []

    for job in job_listings:
        title_element = job.find_element(By.CSS_SELECTOR, ".job-item__title h5")
        job_title = title_element.text.strip()
        job_url = job.get_attribute('href')
        jobs_data.append({"Job-title": job_title, "URL": job_url})

    driver.quit()
    return json.dumps(jobs_data, indent=2)

if __name__ == '__main__':
    html_name = sys.argv[1]
    print(scrape_jobs(html_name))