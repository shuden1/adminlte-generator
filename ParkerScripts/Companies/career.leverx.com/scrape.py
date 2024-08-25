import sys
from selenium import webdriver
import os
from dotenv import load_dotenv

load_dotenv()
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
import threading
import json

# The target HTML file name received from an external source (console command) as the single input parameter
target_html_file = sys.argv[1]

def scrape_job_listings():
    service = ChromeService(executable_path=r""+os.getenv("CHROME_DRIVER_PATH")+"")
    profile_folder_path = os.getenv("CHROME_PROFILE_PATH") + os.path.sep + str(threading.get_ident())
    options = webdriver.ChromeOptions()
    options.add_argument(f"user-data-dir={profile_folder_path}")
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")

    driver = webdriver.Chrome(service=service, options=options)
    driver.get(f"file:///{target_html_file}")

    # Using the selectors identified in STEP 1
    job_cards = driver.find_elements(By.CSS_SELECTOR, ".vacancies__card.vacancies-card")
    job_listings = []

    for card in job_cards:
        job_title = card.find_element(By.CSS_SELECTOR, "h4.vacancies-card__title").text
        job_url = card.find_element(By.CSS_SELECTOR, "a").get_attribute("href")
        job_listings.append({"Job-title": job_title, "URL": job_url})

    driver.quit()

    # Returning the JSON
    return json.dumps(job_listings)

if __name__ == "__main__":
    result = scrape_job_listings()
    print(result)
