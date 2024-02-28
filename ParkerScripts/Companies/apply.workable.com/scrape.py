from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
import shutil
import threading
import sys
import json

# Step 2: Python + Selenium script
def scrape_job_listings(html_file):
    profile_folder_path = "D:\\Mind\\CRA\\AI_Experiments\\Job_Crawlers\\Peter\\adminlte-generator\\chrome_profile\\" + str(threading.get_ident())
    options = Options()
    options.add_argument(f"user-data-dir={profile_folder_path}")
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    service = ChromeService(executable_path=r"C:\Python3\chromedriver.exe")

    driver = webdriver.Chrome(service=service, options=options)
    
    driver.get("file://" + html_file)

    # Revised selectors based on provided HTML structure
    job_listing_selector = ".job-listing"
    job_title_selector = ".job-title"
    job_url_selector = 'a'  # Assuming <a> is the first or the only <a> tag inside the job listing block
    
    # Scrape job listings
    job_elements = driver.find_elements(By.CSS_SELECTOR, job_listing_selector)
    jobs_list = []

    for job_element in job_elements:
        title_element = job_element.find_element(By.CSS_SELECTOR, job_title_selector)
        link_element = job_element.find_element(By.CSS_SELECTOR, job_url_selector)
        job_title = title_element.text
        job_url = link_element.get_attribute('href')
        jobs_list.append({"Job-title": job_title, "URL": job_url})

    driver.quit()
    shutil.rmtree(profile_folder_path)
    
    return json.dumps(jobs_list)

if __name__ == "__main__":
    html_file_path = sys.argv[1]
    print(scrape_job_listings(html_file_path))