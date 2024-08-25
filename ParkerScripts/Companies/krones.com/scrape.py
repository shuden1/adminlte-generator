import sys
import threading
from selenium import webdriver
import os
from dotenv import load_dotenv

load_dotenv()
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import json

def scrape_job_listings(html_file_path):
    profile_folder_path = f"D:\\Mind\\CRA\\AI_Experiments\\Job_Crawlers\\Peter\\adminlte-generator\\chrome_profile\\{threading.get_ident()}"
    service = Service(executable_path=r""+os.getenv("CHROME_DRIVER_PATH")+"")
    options = webdriver.ChromeOptions()
    options.add_argument(f"user-data-dir={profile_folder_path}")
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")

    driver = webdriver.Chrome(service=service, options=options)
    driver.get(f"file:///{html_file_path}")

    # Example selectors, replace with actual ones after analyzing the HTML structure
    listings = driver.find_elements(By.CSS_SELECTOR, ".career-offers--offer")
    job_details = []

    for listing in listings:
        title = listing.find_element(By.CSS_SELECTOR, "a").get_attribute('data-headline')
        url = listing.find_element(By.CSS_SELECTOR, "a").get_attribute('href')
        job_details.append({"Job-title": title, "URL": url})

    driver.quit()

    return json.dumps(job_details)

if __name__ == "__main__":
    html_file_path = sys.argv[1]
    result = scrape_job_listings(html_file_path)
    print(result)
