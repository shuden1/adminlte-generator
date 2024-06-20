import sys
import json
import threading
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup

def main():
    # Get the target HTML file name from the console command
    target_html_file = sys.argv[1]

    # Initialize Chrome options
    profile_folder_path = "D:\\Mind\\CRA\\AI_Experiments\\Job_Crawlers\\Peter\\adminlte-generator\\chrome_profile\\" + str(threading.get_ident())
    chrome_options = Options()
    chrome_options.add_argument(f"user-data-dir={profile_folder_path}")
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")

    # Initialize the Chrome driver
    service = Service(executable_path=r"C:\Python3\chromedriver.exe")
    driver = webdriver.Chrome(service=service, options=chrome_options)

    # Load the HTML file
    driver.get(f"file:///{target_html_file}")

    # Use the selectors defined in STEP 1 to scrape all job listings
    job_blocks = driver.find_elements(By.CSS_SELECTOR, 'div.module--rte')
    job_postings = []

    for job in job_blocks:
        title_element = job.find_element(By.CSS_SELECTOR, 'a[title]')
        url_element = job.find_element(By.CSS_SELECTOR, 'a')
        title = title_element.get_attribute('title')
        url = url_element.get_attribute('href')
        job_postings.append({"Job-title": title, "URL": url})

    # Return the result as JSON
    print(json.dumps(job_postings, indent=4))

    # Close the driver
    driver.quit()

if __name__ == "__main__":
    main()