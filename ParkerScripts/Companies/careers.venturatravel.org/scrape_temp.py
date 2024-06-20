import sys
import json
import threading
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup

def main():
    # Get the HTML file name from the command line argument
    html_file_path = sys.argv[1]

    # Set up the Chrome profile path
    profile_folder_path = f"D:\\Mind\\CRA\\AI_Experiments\\Job_Crawlers\\Peter\\adminlte-generator\\chrome_profile\\{str(threading.get_ident())}"

    # Set up Chrome options
    options = Options()
    options.add_argument(f"user-data-dir={profile_folder_path}")
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")

    # Set up the Chrome driver service
    service = Service(executable_path=r"C:\Python3\chromedriver.exe")

    # Initialize the WebDriver
    driver = webdriver.Chrome(service=service, options=options)

    # Load the HTML file
    driver.get(f"file:///{html_file_path}")

    # Use the selectors defined in STEP 1 to scrape job listings
    job_opening_selector = 'a[href^="/jobs/"]'
    job_title_selector = 'h3.title'

    job_elements = driver.find_elements(By.CSS_SELECTOR, job_opening_selector)
    job_postings = []

    for job_element in job_elements:
        title_element = job_element.find_element(By.CSS_SELECTOR, job_title_selector)
        job_postings.append({
            "Job-title": title_element.text,
            "URL": job_element.get_attribute("href")
        })

    # Close the WebDriver
    driver.quit()

    # Print the JSON result
    print(json.dumps(job_postings, indent=4))

if __name__ == "__main__":
    main()