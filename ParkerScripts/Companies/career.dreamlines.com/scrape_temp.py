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

    # Define the selectors
    job_opening_selector = "div.job_filter"
    job_title_selector = "a.link"
    job_url_selector = "a.link"

    # Find all job openings
    job_openings = driver.find_elements(By.CSS_SELECTOR, job_opening_selector)

    # Extract job titles and URLs
    job_listings = []
    for job in job_openings:
        job_title = job.find_element(By.CSS_SELECTOR, job_title_selector).text
        job_url = job.find_element(By.CSS_SELECTOR, job_url_selector).get_attribute("href")
        job_listings.append({"Job-title": job_title, "URL": job_url})

    # Close the WebDriver
    driver.quit()

    # Print the result as JSON
    print(json.dumps(job_listings, indent=4))

if __name__ == "__main__":
    main()