from selenium import webdriver
import os
from dotenv import load_dotenv

load_dotenv()
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
import threading
import shutil
import sys
import json

# Step 1 selectors from BeautifulSoup analysis
job_listing_container_selector = ".portal-job-listItem"
job_title_selector = "h3.portal-job-tile-title"
job_url_selector = "a.portal-job-tile-link"

# Step 2 script as per instructions
def scrape_job_listings(html_filename):
    service = ChromeService(executable_path=r""+os.getenv("CHROME_DRIVER_PATH")+"")
    profile_folder_path = os.getenv("CHROME_PROFILE_PATH") + os.path.sep + str(threading.get_ident())
    options = Options()
    options.add_argument(f"user-data-dir={profile_folder_path}")
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")

    # Initialize WebDriver
    driver = webdriver.Chrome(service=service, options=options)
    driver.get(f"file://{html_filename}")

    # Scrape job listings
    job_listings = []
    for job_block in driver.find_elements(By.CSS_SELECTOR, job_listing_container_selector):
        title_element = job_block.find_element(By.CSS_SELECTOR, job_title_selector)
        url_element = job_block.find_element(By.CSS_SELECTOR, job_url_selector)
        job_listings.append({
            "Job-title": title_element.text,
            "URL": url_element.get_attribute('href')
        })

    # Close the WebDriver
    driver.quit()

    # Remove the profile folder


    # Return the job listings as JSON
    return json.dumps(job_listings)

# Call function with filename from external argument
if __name__ == "__main__":
    html_file = sys.argv[1]
    print(scrape_job_listings(html_file))
