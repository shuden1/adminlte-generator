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

    # Define the profile folder path
    profile_folder_path = os.getenv("CHROME_PROFILE_PATH") + os.path.sep + str(threading.get_ident())

    # Set up Chrome options
    options = Options()
    options.add_argument(f"user-data-dir={profile_folder_path}")
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")

    # Set up Chrome service
    service = Service(executable_path=r""+os.getenv("CHROME_DRIVER_PATH")+"")

    # Initialize the WebDriver
    driver = webdriver.Chrome(service=service, options=options)

    # Load the HTML file
    driver.get(f"file:///{html_file_path}")

    # Use the selectors defined in Step 1 to scrape job listings
    job_blocks = driver.find_elements(By.CSS_SELECTOR, "div.careers-section-jobs-list-item")
    job_data = []

    for job in job_blocks:
        title_element = job.find_element(By.CSS_SELECTOR, "a.careers-section-jobs-list-item-body-title__link")
        title = title_element.text
        url = title_element.get_attribute("href")
        job_data.append({"Job-title": title, "URL": url})

    # Close the WebDriver
    driver.quit()

    # Print the JSON result
    print(json.dumps(job_data, indent=4))

if __name__ == "__main__":
    main()
