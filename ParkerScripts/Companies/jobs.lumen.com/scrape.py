import shutil
import threading
import json
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By

# STEP 2
def scrape_job_listings(html_file_name):
    # Initialize a headless webdriver
    profile_folder_path = "D:\\Mind\\CRA\\AI_Experiments\\Job_Crawlers\\Peter\\adminlte-generator\\chrome_profile\\" + str(threading.get_ident())
    service = ChromeService(executable_path=r"C:\Python3\chromedriver.exe")
    options = webdriver.ChromeOptions()
    options.add_argument(f"user-data-dir={profile_folder_path}")
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")

    # Start the Chrome browser with the specified options
    driver = webdriver.Chrome(service=service, options=options)

    # Go to the target HTML file
    driver.get(f"file:///{html_file_name}")

    # Use the selectors defined in STEP 1 to scrape job listings
    job_blocks = driver.find_elements(By.CSS_SELECTOR, "ul[class*='au-target'][data-ph-at-id='jobs-list'] li[class*='jobs-list-item']")
    job_listings = []

    for job_block in job_blocks:
        job_title_element = job_block.find_element(By.CSS_SELECTOR, "a[data-ph-at-id='job-link']")
        job_title = job_title_element.text.strip()
        job_url = job_title_element.get_attribute('href').strip()
        job_listings.append({"Job-title": job_title, "URL": job_url})

    # Close the driver and remove the profile folder
    driver.quit()


    # Return the scraped data in JSON format
    return json.dumps(job_listings)

# Retrieve the target HTML file name from the console command input parameter
import sys
if len(sys.argv) == 2:
    html_file_name = sys.argv[1]
    print(scrape_job_listings(html_file_name))
else:
    print('Error: HTML file name argument is required')
