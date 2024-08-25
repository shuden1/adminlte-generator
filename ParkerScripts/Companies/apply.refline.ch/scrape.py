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
    # Get the target HTML file name from the command line argument
    if len(sys.argv) != 2:
        print("Usage: script.py <target_html_file>")
        sys.exit(1)

    target_html_file = sys.argv[1]

    # Set up the ChromeDriver with the specified profile path
    profile_folder_path = f"{os.getenv("CHROME_PROFILE_PATH")}{os.path.sep}{str(threading.get_ident())}"
    service = Service(executable_path=r""+os.getenv("CHROME_DRIVER_PATH")+"")
    options = Options()
    options.add_argument(f"user-data-dir={profile_folder_path}")
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")

    # Initialize the WebDriver
    driver = webdriver.Chrome(service=service, options=options)

    # Load the target HTML file
    driver.get(f"file:///{target_html_file}")

    # Use the selectors defined in STEP 1 to scrape job listings
    job_listings = []
    job_blocks = driver.find_elements(By.CSS_SELECTOR, 'td.position')  # Replace with actual CSS selector

    for job_block in job_blocks:
        job_title_element = job_block.find_element(By.CSS_SELECTOR, 'a')  # Replace with actual CSS selector
        job_url_element = job_block.find_element(By.CSS_SELECTOR, 'a')  # Replace with actual CSS selector

        job_title = job_title_element.text
        job_url = job_url_element.get_attribute('href')

        job_listings.append({"Job-title": job_title, "URL": job_url})

    # Close the WebDriver
    driver.quit()

    # Return the job listings as JSON
    print(json.dumps(job_listings, indent=4))

if __name__ == "__main__":
    main()
