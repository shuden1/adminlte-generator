import sys
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
import threading
import shutil
import json

# STEP 1
# Load the HTML content using BeautifulSoup to identify the structure
html_content = ""  # assuming html_content is loaded with the content from the file

# Parse the HTML content with BeautifulSoup
soup = BeautifulSoup(html_content, 'html.parser')

# Based on 【7†source】 the Job Blocks are located within <ul class="search-results">
# Job Titles are within <h2><a href=URL>Job Title</a></h2>
job_blocks_selector = 'ul.search-results > li.search-result'
job_title_selector = 'h2 a'

# STEP 2
# Create the script based on selectors found
def scrape_jobs(target_html_file):
    # Initialize a headless webdriver
    options = webdriver.ChromeOptions()
    profile_folder_path = "D:\\Mind\\CRA\\AI_Experiments\\Job_Crawlers\\Peter\\adminlte-generator\\chrome_profile\\"+str(threading.get_ident())
    options.add_argument(f"user-data-dir={profile_folder_path}")
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    service = ChromeService(executable_path=r"C:\Python3\chromedriver.exe")
    driver = webdriver.Chrome(service=service, options=options)

    driver.get(f"file:///{target_html_file}")  # Load the local HTML file

    # Scrape all job listings using the previously identified selectors
    job_blocks = driver.find_elements(By.CSS_SELECTOR, job_blocks_selector)
    job_listings = []
    for job in job_blocks:
        job_title = job.find_element(By.CSS_SELECTOR, job_title_selector).text
        job_url = job.find_element(By.CSS_SELECTOR, job_title_selector).get_attribute('href')
        job_listings.append({"Job-title": job_title, "URL": job_url})

    # Output the scraped data as JSON
    json_output = json.dumps(job_listings)
    print(json_output)  # Directly printing the result, not writing to a file

    # At the very end, remove the profile folder
    shutil.rmtree(profile_folder_path, ignore_errors=True)

# Assuming the script is called externally with the HTML filename as an argument
if __name__ == '__main__':
    target_html_file = sys.argv[1]  # The target HTML file passed as an argument
    scrape_jobs(target_html_file)