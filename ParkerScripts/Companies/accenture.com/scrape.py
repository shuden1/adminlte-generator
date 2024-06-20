import sys
import json
import threading
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup

def main():
    # Get the target HTML file name from the command line argument
    html_file_path = sys.argv[1]

    # Initialize ChromeDriver in headless mode with the specified profile path
    profile_folder_path = "D:\\Mind\\CRA\\AI_Experiments\\Job_Crawlers\\Peter\\adminlte-generator\\chrome_profile\\" + str(threading.get_ident())
    service = Service(executable_path=r"C:\Python3\chromedriver.exe")
    options = Options()
    options.add_argument(f"user-data-dir={profile_folder_path}")
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")

    driver = webdriver.Chrome(service=service, options=options)

    # Load the HTML file
    driver.get(f"file:///{html_file_path}")

    # Use the selectors defined in STEP 1 to scrape all job listings
    job_blocks = driver.find_elements(By.CSS_SELECTOR, 'div.rad-filters-vertical__job-card')
    job_openings = []

    for job_block in job_blocks:
        job_title_tag = job_block.find_element(By.CSS_SELECTOR, 'h3.rad-filters-vertical__job-card-title')
        job_url_tag = job_block.find_element(By.CSS_SELECTOR, 'a.rad-filters-vertical__job-card-content-link-button')
        job_title = job_title_tag.text.strip()
        job_url = job_url_tag.get_attribute('href')
        job_openings.append({"Job-title": job_title, "URL": job_url})

    # Close the WebDriver
    driver.quit()

    # Return the JSON with all job postings
    print(json.dumps(job_openings, indent=4))

if __name__ == "__main__":
    main()
