import sys
import json
import threading
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

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

    # Set up the Chrome service
    service = Service(executable_path=r"C:\Python3\chromedriver.exe")

    # Initialize the WebDriver
    driver = webdriver.Chrome(service=service, options=options)

    # Load the HTML file
    driver.get(f"file:///{html_file_path}")

    # Define the selectors
    job_posting_selector = "div.job-posting"
    job_title_selector = "h2.job-title"
    job_url_selector = "a.job-url"

    # Find all job postings
    job_postings = driver.find_elements(By.CSS_SELECTOR, job_posting_selector)

    # Extract job details
    jobs = []
    for job_posting in job_postings:
        job_title_element = job_posting.find_element(By.CSS_SELECTOR, job_title_selector)
        job_title = job_title_element.get_attribute('innerHTML').strip()
        
        job_url_element = job_posting.find_element(By.CSS_SELECTOR, job_url_selector)
        job_url = job_url_element.get_attribute('href') if job_url_element else "#"
        
        jobs.append({"Job-title": job_title, "URL": job_url})

    # Close the WebDriver
    driver.quit()

    # Print the JSON result
    print(json.dumps(jobs, indent=4))

if __name__ == "__main__":
    main()