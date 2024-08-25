from selenium import webdriver
import os
from dotenv import load_dotenv

load_dotenv()
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
import threading
import shutil
import sys
import json

def main(html_file_path):
    # Define CSS selectors based on the BeautifulSoup identification step
    job_listings_selector = '.contentBody h2'
    job_details_selector = '.contentBody h2 + div'

    # Set up headless Chrome WebDriver
    profile_ident = str(threading.get_ident())
    profile_folder_path = f"D:\\Mind\\CRA\\AI_Experiments\\Job_Crawlers\\Peter\\adminlte-generator\\chrome_profile\\{profile_ident}"
    options = webdriver.ChromeOptions()
    options.add_argument(f"user-data-dir={profile_folder_path}")
    options.add_argument("--headless")
    service = ChromeService(executable_path=r""+os.getenv("CHROME_DRIVER_PATH")+"")
    driver = webdriver.Chrome(service=service, options=options)

    # Open local HTML file
    driver.get(f"file:///{html_file_path}")

    # Scrape job listings
    job_elements = driver.find_elements(By.CSS_SELECTOR, job_listings_selector)
    listings = []
    for job_elem in job_elements:
        job_title = job_elem.text.strip()
        try:
            details_elem = job_elem.find_element(By.XPATH, 'following-sibling::div')
            anchor_elem = details_elem.find_element(By.CSS_SELECTOR, 'a')
            job_url = anchor_elem.get_attribute('href')
        except:
            job_url = None
        listings.append({"Job-title": job_title, "URL": job_url})

    driver.quit()

    # Remove the profile folder


    # Print results as JSON
    print(json.dumps(listings, indent=2))


if __name__ == "__main__":
    html_file = sys.argv[1]
    main(html_file)
