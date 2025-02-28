import sys
import json
import shutil
import threading
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

# Step 1: Job opening block and title/URL selectors
job_block_selector = '.card.card-job'
job_title_selector = 'h2.card-title.blue-text a'

# Step 2: Script to scrape job listings
def scrape_job_listings(html_file):
    # Set up Chrome options for headless execution
    options = Options()
    options.headless = True
    options.add_argument("--disable-gpu")
    options.add_argument("--disable-extensions")

    # Set up a new Chrome profile for the current thread
    profile_folder_path = "D:\\Mind\\CRA\\AI_Experiments\\Job_Crawlers\\Peter\\adminlte-generator\\chrome_profile\\" + str(threading.get_ident())

    # Set the service with the ChromeDriver path
    service = ChromeService(executable_path=r"C:\Python3\chromedriver.exe")

    # Initialize the WebDriver with the specified options, service, and profile
    options.add_argument(f"user-data-dir={profile_folder_path}")
    driver = webdriver.Chrome(service=service, options=options)

    # Load the target HTML file
    driver.get(f"file:///{html_file}")

    # Scrape job listings using the selectors provided
    job_listings = []
    for job_block in driver.find_elements(By.CSS_SELECTOR, job_block_selector):
        job_title_element = job_block.find_element(By.CSS_SELECTOR, job_title_selector)
        job_title = job_title_element.text
        job_url = job_title_element.get_attribute('href')
        job_listings.append({"Job-title": job_title, "URL": job_url})

    # Close the WebDriver
    driver.quit()

    # Remove the profile folder
    shutil.rmtree(profile_folder_path)

    # Return the JSON containing job listings
    return json.dumps(job_listings)

# The target HTML file name is an argument sent from an external source
target_html_file = sys.argv[1]

# Call the scraping function and print the result
print(scrape_job_listings(target_html_file))