import sys
import json
import threading
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup

def scrape_jobs(file_path):
    # Initialize Chrome options
    profile_folder_path = "D:\\Mind\\CRA\\AI_Experiments\\Job_Crawlers\\Peter\\adminlte-generator\\chrome_profile\\" + str(threading.get_ident())
    options = Options()
    options.add_argument(f"user-data-dir={profile_folder_path}")
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")

    # Initialize Chrome driver
    service = Service(executable_path=r"C:\Python3\chromedriver.exe")
    driver = webdriver.Chrome(service=service, options=options)

    # Load the HTML file
    driver.get(f"file:///{file_path}")

    # Use the selectors defined in STEP 1 to scrape job listings
    job_blocks = driver.find_elements(By.CSS_SELECTOR, '.css-cq05mv')
    job_openings = []

    for job_block in job_blocks:
        title_tag = job_block.find_element(By.CSS_SELECTOR, 'a.css-zepamx-Anchor')
        job_title = title_tag.text.strip()
        job_url = title_tag.get_attribute('href')
        job_openings.append({"Job-title": job_title, "URL": job_url})

    # Close the driver
    driver.quit()

    # Return the job openings as JSON
    return json.dumps(job_openings, indent=4)

if __name__ == "__main__":
    # Get the file path from the command line argument
    file_path = sys.argv[1]
    job_listings_json = scrape_jobs(file_path)
    print(job_listings_json)
