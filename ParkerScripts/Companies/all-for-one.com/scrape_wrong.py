import sys
from selenium import webdriver
import os
from dotenv import load_dotenv

load_dotenv()
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
import threading
import json

def scrape_jobs(target_html_file):
    # Setup Webdriver
    profile_folder_path = f"D:\\Mind\\CRA\\AI_Experiments\\Job_Crawlers\\Peter\\adminlte-generator\\chrome_profile\\{threading.get_ident()}"
    service = ChromeService(executable_path=r""+os.getenv("CHROME_DRIVER_PATH")+"")
    options = webdriver.ChromeOptions()
    options.add_argument(f"user-data-dir={profile_folder_path}")
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")

    # Initialize Webdriver
    driver = webdriver.Chrome(service=service, options=options)

    # Load the HTML file
    driver.get(f"file:///{target_html_file}")

    # Define correct CSS selectors based on the actual content structure of the HTML file
    # These are placeholders and must be replaced with actual selectors from your HTML document
    job_list_selector = '.job-listing'  # Placeholder for job listings container
    job_title_selector = '.job-title a'  # Placeholder for job title elements
    job_url_attribute = 'href'  # Assuming URLs are contained in href attributes of <a> tags

    # Extract job listings
    job_elements = driver.find_elements(By.CSS_SELECTOR, job_list_selector)
    job_data = []

    for job_element in job_elements:
        title_element = job_element.find_element(By.CSS_SELECTOR, job_title_selector)
        title = title_element.text
        url = title_element.get_attribute(job_url_attribute)
        job_data.append({"Job-title": title, "URL": url})

    # Output the job listings as JSON
    print(json.dumps(job_data))

    # Cleanup
    driver.quit()

if __name__ == "__main__":
    target_html_file = sys.argv[1]
    scrape_jobs(target_html_file)
