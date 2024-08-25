import sys
import json
import threading
from selenium import webdriver
import os
from dotenv import load_dotenv

load_dotenv()
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup

def scrape_jobs(file_path):
    # Initialize Chrome options
    profile_folder_path = os.getenv("CHROME_PROFILE_PATH") + os.path.sep + str(threading.get_ident())
    options = Options()
    options.add_argument(f"user-data-dir={profile_folder_path}")
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")

    # Initialize Chrome driver
    service = Service(executable_path=r""+os.getenv("CHROME_DRIVER_PATH")+"")
    driver = webdriver.Chrome(service=service, options=options)

    # Load the HTML file
    driver.get(f"file:///{file_path}")

    # Use BeautifulSoup to parse the page source
    soup = BeautifulSoup(driver.page_source, 'html.parser')

    # Find job listings using the selectors defined in Step 1
    job_openings = []
    job_table = soup.find('table', class_='searchResults')

    if job_table:
        job_rows = job_table.find('tbody').find_all('tr')
        for job_row in job_rows:
            job_title_tag = job_row.find('a', class_='jobTitle-link')
            if job_title_tag:
                job_title = job_title_tag.get_text(strip=True)
                job_url = job_title_tag['href']
                job_openings.append({"Job-title": job_title, "URL": job_url})

    # Close the driver
    driver.quit()

    # Return the job listings as JSON
    return json.dumps(job_openings, indent=4)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script.py <path_to_html_file>")
        sys.exit(1)

    file_path = sys.argv[1]
    job_listings_json = scrape_jobs(file_path)
    print(job_listings_json)
