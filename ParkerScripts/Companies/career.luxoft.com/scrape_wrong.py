import sys
import threading
from selenium import webdriver
import os
from dotenv import load_dotenv

load_dotenv()
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By

def scrape_job_listings(html_file_name):
    service = ChromeService(executable_path=r""+os.getenv("CHROME_DRIVER_PATH")+"")
    profile_folder_path = os.getenv("CHROME_PROFILE_PATH") + os.path.sep + str(threading.get_ident())
    options = webdriver.ChromeOptions()
    options.add_argument(f"user-data-dir={profile_folder_path}")
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")

    driver = webdriver.Chrome(service=service, options=options)
    driver.get(f"file:///{html_file_name}")

    jobs = []
    # The selectors need to precisely match elements in the HTML structure containing job listings.
    job_listings = driver.find_elements(By.CSS_SELECTOR, "div.job-listing, li.job-opening")  # Updated selector as an example
    for job in job_listings:
        title_element = job.find_element(By.CSS_SELECTOR, "h3 > a, .job-title a")  # Updated selector as an example
        job_title = title_element.text.strip()
        job_url = title_element.get_attribute("href").strip()
        jobs.append({"Job-title": job_title, "URL": job_url})

    driver.quit()
    print({"jobs": jobs})  # Changed the output formatting to match the requested JSON structure.

if __name__ == "__main__":
    html_file_path = sys.argv[1]  # Assumes the HTML file path is passed as the first argument.
    scrape_job_listings(html_file_path)
