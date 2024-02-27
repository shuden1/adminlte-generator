import sys
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import threading
import shutil
import json

def scrape_job_listings(html_file_path):
    # Define selectors for job blocks
    job_block_selector = ".jobs-list-item"
    job_title_url_selector = "[data-ph-at-id='job-link']"
    
    # Step 2: Initialize Chrome in headless mode.
    chrome_options = Options()
    chrome_options.add_argument("--headless")

    profile_folder_path = "D:\\Mind\\CRA\\AI_Experiments\\Job_Crawlers\\Peter\\adminlte-generator\\chrome_profile\\" \
                          + str(threading.get_ident())

    chrome_options.add_argument(f"user-data-dir={profile_folder_path}")
    service = ChromeService(executable_path=r"C:\Python3\chromedriver.exe")

    driver = webdriver.Chrome(service=service, options=chrome_options)

    # Step 3: Open the HTML file.
    driver.get(f"file:///{html_file_path}")

    # Step 4: Scrape job listings.
    job_elements = driver.find_elements(By.CSS_SELECTOR, job_block_selector)
    job_listings = []

    for job_elem in job_elements:
        title_elem = job_elem.find_element(By.CSS_SELECTOR, job_title_url_selector)
        job_title = title_elem.text.strip()
        job_url = title_elem.get_attribute('href')
        job_listings.append({"Job-title": job_title, "URL": job_url})

    # Step 5: Return JSON of job listings.
    job_listings_json = json.dumps(job_listings)

    # Step 6: Clean up by closing the driver and removing the profile folder.
    driver.quit()
    shutil.rmtree(profile_folder_path)

    return job_listings_json

if __name__ == "__main__":
    html_filename = sys.argv[1]
    print(scrape_job_listings(html_filename))