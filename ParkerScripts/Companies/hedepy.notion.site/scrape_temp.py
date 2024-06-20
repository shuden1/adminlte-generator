import sys
import json
import threading
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

def scrape_jobs(file_path):
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

    # Open the HTML file
    driver.get(f"file:///{file_path}")

    # Selectors for job openings, titles, and URLs
    job_opening_selector = 'div.notion-selectable.notion-text-block'
    job_title_selector = 'a.notion-link-token'

    # Scrape job listings
    job_elements = driver.find_elements(By.CSS_SELECTOR, job_opening_selector)
    job_data = []
    for job_element in job_elements:
        title_element = job_element.find_element(By.CSS_SELECTOR, job_title_selector)
        job_data.append({
            "Job-title": title_element.text,
            "URL": title_element.get_attribute('href')
        })

    # Close the driver
    driver.quit()

    # Return the job data as JSON
    return json.dumps(job_data, indent=4)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script.py <path_to_html_file>")
        sys.exit(1)

    file_path = sys.argv[1]
    job_listings_json = scrape_jobs(file_path)
    print(job_listings_json)
