from selenium import webdriver
import os
from dotenv import load_dotenv

load_dotenv()
from selenium.webdriver.common.by import By
import threading
import sys
import json

def scrape_job_listings(target_html):
    # Profile path configuration
    profile_folder_path = os.getenv("CHROME_PROFILE_PATH") + "\\" + str(threading.get_ident())

    # Chrome options configuration
    options = webdriver.ChromeOptions()
    options.add_argument(f"user-data-dir={profile_folder_path}")
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")

    # Service configuration
    service = webdriver.chrome.service.Service(executive_path=r""+os.getenv("CHROME_DRIVER_PATH")+"")

    # Initialize WebDriver
    driver = webdriver.Chrome(service=service, options=options)

    # Load the target HTML file
    driver.get(f"file:///{target_html}")

    # Scraping job listings using defined selectors
    job_blocks = driver.find_elements(By.CSS_SELECTOR, "li.css-1q2dra3")
    job_data = []
    for job in job_blocks:
        title_element = job.find_elements(By.CSS_SELECTOR, "h3 > a.css-19uc56f")[0]
        title = title_element.text
        url = title_element.get_attribute("href")
        job_data.append({"Job-title": title, "URL": url})

    # Quit the driver session
    driver.quit()

    # Output the scraped data as JSON
    return json.dumps(job_data, indent=2)

if __name__ == "__main__":
    # Checking if an argument (target HTML file path) is passed
    if len(sys.argv) != 2:
        print("Incorrect number of arguments. Please provide the path to the target HTML file.")
    else:
        target_html = sys.argv[1]
        print(scrape_job_listings(target_html))
