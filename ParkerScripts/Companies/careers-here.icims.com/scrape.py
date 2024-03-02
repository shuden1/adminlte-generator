import threading
import shutil
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
import sys

# STEP 2: Selenium automation script
def scrape_job_listings(html_file_path):
    # Create a profile folder path based on the current thread id
    profile_folder_path = "D:\\Mind\\CRA\\AI_Experiments\\Job_Crawlers\\Peter\\adminlte-generator\\chrome_profile\\" + str(threading.get_ident())

    # Set up Chrome service and options for headless browsing
    service = Service(executable_path=r"C:\Python3\chromedriver.exe")
    options = webdriver.ChromeOptions()
    options.add_argument(f"user-data-dir={profile_folder_path}")
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")

    # Initialize and configure the headless webdriver
    driver = webdriver.Chrome(service=service, options=options)
    driver.get(f"file:///{html_file_path}")

    # Define the CSS selectors for job titles and URLs
    job_listing_selector = 'div.navigation-link:not(.overview)'
    job_title_selector = 'span.link-text'
    job_url_selector = 'a.link-only'

    # Scrape all job listings based on the defined selectors
    jobs = []
    job_elements = driver.find_elements(By.CSS_SELECTOR, job_listing_selector)
    for job_element in job_elements:
        title_element = job_element.find_element(By.CSS_SELECTOR, job_title_selector)
        url_element = job_element.find_element(By.CSS_SELECTOR, job_url_selector)
        jobs.append({
            "Job-title": title_element.get_attribute('data-title').strip(),
            "URL": url_element.get_attribute('href')
        })

    # Quit the driver and clean up the profile folder
    driver.quit()
    # shutil.rmtree(profile_folder_path, ignore_errors=True)

    # Return the list of jobs in JSON format
    return json.dumps(jobs)

# Get the target HTML file name from command line argument
if __name__ == "__main__":
    html_file_path = sys.argv[1]
    print(scrape_job_listings(html_file_path))
