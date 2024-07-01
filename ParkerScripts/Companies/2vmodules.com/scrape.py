import sys
import json
import threading
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options

def main():
    # Get the HTML file name from the command line argument
    html_file = sys.argv[1]

    # Define the profile folder path
    profile_folder_path = "D:\\Mind\\CRA\\AI_Experiments\\Job_Crawlers\\Peter\\adminlte-generator\\chrome_profile\\" + str(threading.get_ident())

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

    try:
        # Load the HTML file
        driver.get(f"file:///{html_file}")

        # Define the selectors
        job_opening_selector = "div.career-block_career_block_text__LSEBl"
        job_title_selector = "span"
        job_url_selector = "a.button.button-dark.button-envelop"

        # Find all job postings
        job_postings = driver.find_elements(By.CSS_SELECTOR, job_opening_selector)
        jobs = []

        for job in job_postings:
            try:
                # Extract job title
                job_title_element = job.find_element(By.CSS_SELECTOR, job_title_selector)
                job_title = job_title_element.text.strip()
                if not job_title:
                    job_title = job_title_element.get_attribute('innerHTML').strip()

                # Extract job URL
                try:
                    job_url_element = job.find_element(By.CSS_SELECTOR, job_url_selector)
                    job_url = job_url_element.get_attribute('href')
                except NoSuchElementException:
                    job_url = "#"

                # Append job details to the list
                jobs.append({"Job-title": job_title, "URL": job_url})

            except NoSuchElementException:
                continue

        # Print the JSON result
        print(json.dumps(jobs, indent=4))

    finally:
        # Quit the WebDriver
        driver.quit()

if __name__ == "__main__":
    main()