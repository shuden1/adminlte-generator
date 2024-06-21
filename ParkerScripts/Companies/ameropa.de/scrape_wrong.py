import sys
import json
import threading
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

def main():
    # Get the HTML file name from the command line argument
    html_file = sys.argv[1]

    # Set up the Chrome profile path
    profile_folder_path = "D:\\Mind\\CRA\\AI_Experiments\\Job_Crawlers\\Peter\\adminlte-generator\\chrome_profile\\" + str(threading.get_ident())

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
    driver.get(f"file:///{html_file}")

    # Find all job postings
    job_elements = driver.find_elements(By.CSS_SELECTOR, "div.job-offer")

    job_listings = []

    for job_element in job_elements:
        # Extract job title
        job_title_element = job_element.find_element(By.CSS_SELECTOR, "h2.job-title")
        job_title = job_title_element.get_attribute('innerHTML').strip()

        # Extract job URL
        try:
            job_url_element = job_element.find_element(By.CSS_SELECTOR, "a.job-url")
            job_url = job_url_element.get_attribute('href')
        except:
            job_url = "#"

        job_listings.append({"Job-title": job_title, "URL": job_url})

    # Close the WebDriver
    driver.quit()

    # Print the job listings as JSON
    print(json.dumps(job_listings, indent=4))

if __name__ == "__main__":
    main()