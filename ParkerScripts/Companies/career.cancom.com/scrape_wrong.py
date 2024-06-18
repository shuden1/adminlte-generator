import sys
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
import json
import threading
import re

def scrape_jobs(html_file_path):
    profile_folder_path = f"D:\\Mind\\CRA\\AI_Experiments\\Job_Crawlers\\Peter\\adminlte-generator\\chrome_profile\\{threading.get_ident()}"
    chrome_service = Service(executable_path=r"C:\Python3\chromedriver.exe")
    options = webdriver.ChromeOptions()
    options.add_argument(f"user-data-dir={profile_folder_path}")
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")

    driver = webdriver.Chrome(service=chrome_service, options=options)
    job_cards = driver.find_elements(By.CSS_SELECTOR, ".search_result")
    job_listings = []
    print(job_cards)
    for card in job_cards:
        job_title = card.find_element(By.CSS_SELECTOR, "h2.vc_headline.has-fontsize-h6").text
        print(job_title)
        onclick_attr = card.find_element(By.CSS_SELECTOR, "vc-content-box").get_attribute("onclick")

        # Use regex to extract the URL
        url_match = re.search(r'window.open\("([^"]*)', onclick_attr)
        # Check if a match was found
        if url_match:
            job_url = url_match.group(1)
        else:
            job_url = None
        job_listings.append({"Job-title": job_title, "URL": job_url})

    driver.quit()
    return json.dumps(job_listings)

# For illustration purposes, actual HTML file path should be replaced by sys.argv[1]
html_file_path = sys.argv[1]
jobs_data = scrape_jobs(html_file_path)
print(json.dumps(jobs_data))
