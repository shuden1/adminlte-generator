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

    # Set up the Chrome profile path
    profile_folder_path = os.getenv("CHROME_PROFILE_PATH") + os.path.sep + str(threading.get_ident())

    # Set up Chrome options
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

    # Use the selectors defined in STEP 1 to find job listings
    job_blocks = driver.find_elements(By.CSS_SELECTOR, 'article.style_vacancy_details_container__ACeFx')
    job_openings = []

    for job_block in job_blocks:
        title_element = job_block.find_element(By.CSS_SELECTOR, 'h2.style_vacancy_title__892Tj')
        job_title = title_element.text
        url_element = job_block.find_element(By.CSS_SELECTOR, 'a')  # Assuming the URL is within an <a> tag inside the job block
        job_url = url_element.get_attribute('href')
        job_openings.append({"Job-title": job_title, "URL": job_url})

    # Close the WebDriver
    driver.quit()

    # Print the result as JSON
    print(json.dumps(job_openings, indent=4))

if __name__ == "__main__":
    main()
