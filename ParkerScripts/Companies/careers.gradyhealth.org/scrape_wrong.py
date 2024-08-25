import sys
from selenium import webdriver
import os
from dotenv import load_dotenv

load_dotenv()
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
import threading
import json

def scrape_job_listings(file_name):
    profile_folder_path = os.getenv("CHROME_PROFILE_PATH") + "\\" + str(threading.get_ident())
    service = ChromeService(executable_path=r""+os.getenv("CHROME_DRIVER_PATH")+"")
    options = webdriver.ChromeOptions()
    options.add_argument(f"user-data-dir={profile_folder_path}")
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")

    driver = webdriver.Chrome(service=service, options=options)
    driver.get(f"file:///{file_name}")

    job_listings = []
    # This is a place where actual selectors should be placed based on the HTML file structure
    # Example selectors are placeholders and need to be replaced based on Step 1 analysis
    job_elements = driver.find_elements(By.CSS_SELECTOR, "div.job_listing")  # Example selector
    for job_element in job_elements:
        title_element = job_element.find_element(By.CSS_SELECTOR, "a.title")  # Example selector
        url_element = title_element.get_attribute('href')  # Assuming 'a.title' contains the link
        job_listings.append({"Job-title": title_element.text, "URL": url_element})

    driver.quit()
    return json.dumps(job_listings, indent=4)

if __name__ == "__main__":
    if len(sys.argv) > 1:
        file_name = sys.argv[1]
        scraped_jobs = scrape_job_listings(file_name)
        print(scraped_jobs)
    else:
        print("No file name provided.")
