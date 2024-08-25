import sys
from selenium import webdriver
import os
from dotenv import load_dotenv

load_dotenv()
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
import threading
import json
import shutil

# Step 1: Modified results from BeautifulSoup (from error message observation)
job_listing_selector = "section.section"
job_title_selector = ".col-inner h1.entry-title, .col-inner h2"  # Modified selector for job titles
job_url_selector = ".col-inner a.button.secondary"  # Modified selector for job URLs

# Step 2: Modified Selenium script
def scrape_job_listings(target_html_file):
    profile_folder_path = os.getenv("CHROME_PROFILE_PATH") + "\\" + str(threading.get_ident())
    service = ChromeService(executable_path=r""+os.getenv("CHROME_DRIVER_PATH")+"")
    options = webdriver.ChromeOptions()
    options.add_argument(f"user-data-dir={profile_folder_path}")
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")

    driver = webdriver.Chrome(service=service, options=options)
    driver.get(f"file://{target_html_file}")

    job_listings = []
    job_blocks = driver.find_elements(by=By.CSS_SELECTOR, value=job_listing_selector)
    for block in job_blocks:
        job_titles = block.find_elements(by=By.CSS_SELECTOR, value=job_title_selector)
        job_links = block.find_elements(by=By.CSS_SELECTOR, value=job_url_selector)
        for title, link in zip(job_titles, job_links):
            job_listings.append({"Job-title": title.text.strip(), "URL": link.get_attribute('href').strip()})

    driver.quit()


    return json.dumps(job_listings)

if __name__ == '__main__':
    html_file_name = sys.argv[1]
    print(scrape_job_listings(html_file_name))
