from bs4 import BeautifulSoup
import sys
import json
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import threading
import shutil

# BeautifulSoup Part for Selectors (Step 1)
with open(sys.argv[1], 'r', encoding='utf-8') as file:
    html_content = file.read()
    soup = BeautifulSoup(html_content, 'html.parser')

# Identifying the EXACT HTML selectors for job openings, titles, and URLs.
# This is simulated logic based on the example given in the file.
job_listing_selector = "div.tab-pane"
job_title_url_selector = "h3 strong"

# Selenium Part for Web Scraping (Step 2)
def main(html_file):
    profile_folder_path = "D:\\Mind\\CRA\\AI_Experiments\\Job_Crawlers\\Peter\\adminlte-generator\\chrome_profile\\" + str(threading.get_ident())
    service = ChromeService(executable_path=r"C:\Python3\chromedriver.exe")
    options = Options()
    options.add_argument(f"user-data-dir={profile_folder_path}")
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")

    driver = webdriver.Chrome(service=service, options=options)

    # Scrape job listings.
    driver.get(f'file:///{html_file}')
    jobs = []
    listings = driver.find_elements(By.CSS_SELECTOR, job_listing_selector)
    for listing in listings:
        job_titles = listing.find_elements(By.CSS_SELECTOR, job_title_url_selector)
        for title in job_titles:
            jobs.append({
                "Job-title": title.text.strip(),
                "URL": "#"
            })

    driver.quit()

    # Remove the profile folder after quitting the driver


    return json.dumps(jobs)

if __name__ == "__main__":
    html_filename = sys.argv[1]
    print(main(html_filename))
