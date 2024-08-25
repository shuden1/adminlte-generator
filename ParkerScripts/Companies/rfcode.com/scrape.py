import sys
from selenium import webdriver
import os
from dotenv import load_dotenv

load_dotenv()
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
import threading
import shutil
import json

def scrape_job_listings(html_file_path):
    # Initialize the Chrome driver
    profile_folder_path = os.getenv("CHROME_PROFILE_PATH") + "\\" + str(threading.get_ident())
    service = ChromeService(executable_path=r""+os.getenv("CHROME_DRIVER_PATH")+"")
    options = webdriver.ChromeOptions()
    options.add_argument(f"user-data-dir={profile_folder_path}")
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    driver = webdriver.Chrome(service=service, options=options)

    # Open the HTML file
    driver.get(f"file://{html_file_path}")

    # Scrape job listings
    job_listings = []
    # Use the previously identified job listings block and job title & URL selectors
    job_blocks = driver.find_elements(By.CSS_SELECTOR, ".bg--gray")
    for block in job_blocks:
        titles = block.find_elements(By.CSS_SELECTOR, "h1")
        for title in titles:
            job = {
                "Job-title": title.text,
                "URL": title.find_element(By.XPATH, ".//following-sibling::p/a").get_attribute("href") if title.find_element(By.XPATH, ".//following-sibling::p/a") else ""
            }
            job_listings.append(job)

    # Close the driver
    driver.quit()

    # Remove the profile folder


    # Convert the job listings to JSON and return
    return json.dumps(job_listings)

if __name__ == "__main__":
    file_name = sys.argv[1]
    print(scrape_job_listings(file_name))
