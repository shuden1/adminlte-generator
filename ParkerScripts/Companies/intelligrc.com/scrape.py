from selenium import webdriver
import os
from dotenv import load_dotenv

load_dotenv()
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import json
import shutil
import sys
import threading

# Function to scrape job listings
def scrape_job_listings(html_file):
    # Profile path and service setup
    profile_folder_path = f"{os.getenv("CHROME_PROFILE_PATH")}{os.path.sep}{threading.get_ident()}"
    service = Service(executable_path=r""+os.getenv("CHROME_DRIVER_PATH")+"")
    options = webdriver.ChromeOptions()
    options.add_argument(f"user-data-dir={profile_folder_path}")
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")

    # Selenium driver initialization
    driver = webdriver.Chrome(service=service, options=options)

    # Reading HTML file content
    with open(html_file, 'r', encoding='utf-8') as file:
        content = file.read()

    # Get HTML content with driver
    driver.get("data:text/html;charset=utf-8," + content)

    # Scrape Job Listings and URLs
    job_listings = []
    positions = driver.find_elements(By.CSS_SELECTOR, ".benefits-item.positions")
    for position in positions:
        print(position)
        title_element = position.find_element(By.CSS_SELECTOR, "h3.text-size-regular.text-weight-bold.text-color-neutral-900")
        job_title = title_element.textContent
        link_element = position.find_element(By.CSS_SELECTOR, "a")  # Assuming there is an <a> tag
        job_url = link_element.get_attribute("href") if link_element else "https://www.intelligrc.com/careers"
        job_listings.append({"Job-title": job_title, "URL": job_url})

    # Quit driver and cleanup profile
    driver.quit()


    # Return job listings as JSON
    return json.dumps(job_listings)

# Main execution
if __name__ == "__main__":
    html_filename = sys.argv[1]
    job_listings_json = scrape_job_listings(html_filename)
    print(job_listings_json)
