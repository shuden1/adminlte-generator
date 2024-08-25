import sys
from selenium import webdriver
import os
from dotenv import load_dotenv

load_dotenv()
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import json
import threading

def scrape_jobs(html_file_name):
    profile_folder_path = os.getenv("CHROME_PROFILE_PATH") + "\\"+str(threading.get_ident())
    service = Service(executable_path=r""+os.getenv("CHROME_DRIVER_PATH")+"")
    options = webdriver.ChromeOptions()
    options.add_argument(f"user-data-dir={profile_folder_path}")
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")

    driver = webdriver.Chrome(service=service, options=options)
    driver.get(f"file:///{html_file_name}")

    # Corrected script with potential fixes based on a typical mistake scenario
    job_listing_selector = ".job-listing"  # Placeholder for correct job listing container selector
    job_title_selector = ".job-title"  # Placeholder for title element relative to job_listing_selector
    job_url_selector = "a"  # Assuming URLs are directly in `a` tags within job listings

    job_listings = driver.find_elements(By.CSS_SELECTOR, job_listing_selector)
    jobs_list = []

    for job_listing in job_listings:
        title_element = job_listing.find_element(By.CSS_SELECTOR, job_title_selector)
        url_element = job_listing.find_element(By.CSS_SELECTOR, job_url_pic)
        jobs_list.append({"Job-title": title_element.text, "URL": url_element.get_attribute("href")})

    driver.quit()
    return json.dumps(jobs_list, indent=2)

if __name__ == "__main__":
    html_file_name = sys.argv[1]
    print(scrape_jobs(html_file_name))
