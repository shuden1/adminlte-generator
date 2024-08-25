import sys
from selenium import webdriver
import os
from dotenv import load_dotenv

load_dotenv()
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
import threading
import json

# Step 2: Implement Selenium script
def scrape_jobs(html_file):
    # Preparing the Chrome service
    service = ChromeService(executable_path=r""+os.getenv("CHROME_DRIVER_PATH")+"")
    profile_folder_path = os.getenv("CHROME_PROFILE_PATH") + os.path.sep + str(threading.get_ident())
    options = webdriver.ChromeOptions()
    options.add_argument(f"user-data-dir={profile_folder_path}")
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")

    # Initializing the Chrome Web Driver
    driver = webdriver.Chrome(service=service, options=options)

    # Open the HTML file
    driver.get(f"file:///{html_file}")

    # Scraping job listings
    jobs = []
    # Since no specific selectors were found in the provided HTML, the pseudo codification of next steps is mentioned.
    # Replace below line with actual scraping logic using selectors identified in Step 1
    job_elements = driver.find_elements(By.CSS_SELECTOR, "selector_for_job_listings")

    for job_element in job_elements:
        title = job_element.find_element(By.CSS_SELECTOR, "selector_for_job_title").text
        url = job_element.find_element(By.CSS_SELECTOR, "selector_for_job_url").get_attribute("href")
        jobs.append({"Job-title": title, "URL": url})

    driver.close()

    # Output the scraped data
    return json.dumps(jobs, ensure_ascii=False)

if __name__ == "__main__":
    html_file_path = sys.argv[1]
    print(scrape_jobs(html_file_path))
