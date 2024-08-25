import sys
import json
import threading
from selenium import webdriver
import os
from dotenv import load_dotenv

load_dotenv()
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

def main():
    # Get the HTML file name from the command line argument
    html_file_path = sys.argv[1]

    # Set up the Chrome options
    profile_folder_path = f"D:\\Mind\\CRA\\AI_Experiments\\Job_Crawlers\\Peter\\adminlte-generator\\chrome_profile\\{str(threading.get_ident())}"
    options = Options()
    options.add_argument(f"user-data-dir={profile_folder_path}")
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")

    # Set up the Chrome service
    service = Service(executable_path=r""+os.getenv("CHROME_DRIVER_PATH")+"")

    # Initialize the WebDriver
    driver = webdriver.Chrome(service=service, options=options)

    # Load the HTML file
    driver.get(f"file:///{html_file_path}")

    # Define the selectors
    job_posting_selector = 'div.vacancies-item'
    job_title_selector = 'h2.vacancies-item-title'
    job_url_selector = 'a.vacancies-item-link'

    # Find all job postings
    job_postings = driver.find_elements(By.CSS_SELECTOR, job_posting_selector)

    # Extract job details
    jobs = []
    for job in job_postings:
        title_element = job.find_element(By.CSS_SELECTOR, job_title_selector)
        title = title_element.get_attribute('innerHTML').strip()

        url_elements = job.find_elements(By.CSS_SELECTOR, job_url_selector)
        url = url_elements[0].get_attribute('href') if url_elements else "#"

        jobs.append({"Job-title": title, "URL": url})

    # Close the WebDriver
    driver.quit()

    # Print the result as JSON
    print(json.dumps(jobs, ensure_ascii=False, indent=4))

if __name__ == "__main__":
    main()
