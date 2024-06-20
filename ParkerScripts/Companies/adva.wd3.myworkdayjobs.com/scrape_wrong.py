import sys
import json
import threading
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

def scrape_jobs(html_file_path):
    # Initialize Chrome options
    profile_folder_path = f"D:\\Mind\\CRA\\AI_Experiments\\Job_Crawlers\\Peter\\adminlte-generator\\chrome_profile{str(threading.get_ident())}"
    options = Options()
    options.add_argument(f"user-data-dir={profile_folder_path}")
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")

    # Initialize Chrome service
    service = Service(executable_path=r"C:\Python3\chromedriver.exe")

    # Initialize WebDriver
    driver = webdriver.Chrome(service=service, options=options)

    # Load the HTML file
    driver.get(f"file:///{html_file_path}")

    # Scrape job listings using the selectors defined in STEP 1
    job_listings = []
    job_blocks = driver.find_elements(By.CSS_SELECTOR, 'div[class*="job"]')  # Example selector, adjust based on actual HTML structure
    for job_block in job_blocks:
        title_element = job_block.find_element(By.CSS_SELECTOR, 'a')  # Example selector, adjust based on actual HTML structure
        job_title = title_element.text
        job_url = title_element.get_attribute('href')
        job_listings.append({"Job-title": job_title, "URL": job_url})

    # Close the WebDriver
    driver.quit()

    # Return the job listings as JSON
    return json.dumps(job_listings, indent=4)

if __name__ == "__main__":
    # Get the HTML file path from the command line argument
    html_file_path = sys.argv[1]
    # Scrape the jobs and print the result
    print(scrape_jobs(html_file_path))