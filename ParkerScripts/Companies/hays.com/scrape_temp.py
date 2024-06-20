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

    # Define the profile folder path
    profile_folder_path = f"D:\\Mind\\CRA\\AI_Experiments\\Job_Crawlers\\Peter\\adminlte-generator\\chrome_profile{str(threading.get_ident())}"

    # Set up Chrome options
    options = Options()
    options.add_argument(f"user-data-dir={profile_folder_path}")
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")

    # Set up Chrome service
    service = Service(executable_path=r"C:\Python3\chromedriver.exe")

    # Initialize the WebDriver
    driver = webdriver.Chrome(service=service, options=options)

    # Load the HTML file
    driver.get(f"file:///{html_file_path}")

    # Use BeautifulSoup to parse the HTML content
    soup = BeautifulSoup(driver.page_source, 'html.parser')

    # Define the selectors
    job_block_selector = 'div[class*="job"]'
    job_title_selector = 'a[class*="jobTitle"] h3'
    job_url_selector = 'a[class*="jobTitle"]'

    # Find job blocks
    job_blocks = driver.find_elements(By.CSS_SELECTOR, job_block_selector)

    # Extract job titles and URLs
    job_openings = []
    for job_block in job_blocks:
        title_element = job_block.find_element(By.CSS_SELECTOR, job_title_selector)
        url_element = job_block.find_element(By.CSS_SELECTOR, job_url_selector)
        job_title = title_element.text
        job_url = url_element.get_attribute('href')
        job_openings.append({"Job-title": job_title, "URL": job_url})

    # Close the WebDriver
    driver.quit()

    # Print the result as JSON
    print(json.dumps(job_openings, indent=4))

if __name__ == "__main__":
    main()