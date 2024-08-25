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
    html_file = sys.argv[1]

    # Set up the ChromeDriver with the specified profile path and options
    profile_folder_path = f"D:\\Mind\\CRA\\AI_Experiments\\Job_Crawlers\\Peter\\adminlte-generator\\chrome_profile\\{str(threading.get_ident())}"
    service = Service(executable_path=r"C:\\Python3\\chromedriver.exe")
    options = Options()
    options.add_argument(f"user-data-dir={profile_folder_path}")
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")

    # Initialize the WebDriver
    driver = webdriver.Chrome(service=service, options=options)

    # Load the HTML file
    driver.get(f"file:///{html_file}")

    # Define the selectors for job blocks, titles, and URLs
    job_block_selector = "[class*='job'], [class*='career'], [class*='opening'], [class*='position']"  # Replace with the correct class or parameter
    job_title_selector = "a"  # Replace with the correct class or parameter if necessary

    # Find all job blocks
    job_blocks = driver.find_elements(By.CSS_SELECTOR, job_block_selector)

    # Extract job titles and URLs
    job_postings = []
    for job in job_blocks:
        title_element = job.find_element(By.CSS_SELECTOR, job_title_selector)
        job_postings.append({
            "Job-title": title_element.text,
            "URL": title_element.get_attribute("href")
        })

    # Close the WebDriver
    driver.quit()

    # Print the job postings as JSON
    print(json.dumps(job_postings, ensure_ascii=False, indent=4))

if __name__ == "__main__":
    main()
