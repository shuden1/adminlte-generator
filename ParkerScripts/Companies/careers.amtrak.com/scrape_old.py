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

    # Set up Chrome options
    profile_folder_path = f"D:\\Mind\\CRA\\AI_Experiments\\Job_Crawlers\\Peter\\adminlte-generator\\chrome_profile\\{str(threading.get_ident())}"
    chrome_options = Options()
    chrome_options.add_argument(f"user-data-dir={profile_folder_path}")
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")

    # Set up Chrome service
    service = Service(executable_path=r""+os.getenv("CHROME_DRIVER_PATH")+"")

    # Initialize the WebDriver
    driver = webdriver.Chrome(service=service, options=chrome_options)

    # Load the HTML file
    driver.get(f"file:///{html_file_path}")

    # Define the selectors for job blocks, titles, and URLs
    job_block_selector = ".data-row"
    job_title_selector = ".jobTitle-link"

    # Find all job blocks
    job_blocks = driver.find_elements(By.CSS_SELECTOR, job_block_selector)

    # Extract job titles and URLs
    jobs = []
    for job_block in job_blocks:
        title_element = job_block.find_element(By.CSS_SELECTOR, job_title_selector)
        title = title_element.text
        url = title_element.get_attribute("href")
        jobs.append({"Job-title": title, "URL": url})

    # Return the JSON result
    print(json.dumps(jobs, indent=4))

    # Close the WebDriver
    driver.quit()

if __name__ == "__main__":
    main()
