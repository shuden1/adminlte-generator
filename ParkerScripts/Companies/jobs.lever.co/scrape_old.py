from bs4 import BeautifulSoup
import json
import sys
from selenium import webdriver
import os
from dotenv import load_dotenv

load_dotenv()
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service

# STEP 2
def scrape_job_listings(html_file):
    # Read the provided HTML file
    with open(html_file, 'r') as file:
        content = file.read()

    # Parse content using BeautifulSoup
    soup = BeautifulSoup(content, 'html.parser')

    # STEP 1
    # Identifying the EXACT HTML selectors including classes representing the blocks with Job Openings
    job_blocks_selector = '.postings-group div.posting'
    # Identifying the EXACT selectors for job titles and their associated URLs
    job_title_selector = 'h5[data-qa="posting-name"]'
    job_url_selector = 'a.posting-title'

    # Initialize the WebDriver
    profile_folder_path = os.getenv("CHROME_PROFILE_PATH") + "\\" + str(threading.get_ident())
    service = Service(executable_path=r""+os.getenv("CHROME_DRIVER_PATH")+"")

    options = webdriver.ChromeOptions()
    options.add_argument(f"user-data-dir={profile_folder_path}")
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")

    driver = webdriver.Chrome(service=service, options=options)
    driver.get(f"file://{html_file}")

    # Find all Job Opening Blocks
    job_blocks = soup.select(job_blocks_selector)

    # Prepare the list that will contain the job details
    jobs = []

    # Loop through all job blocks and scrape the necessary information
    for job_block in job_blocks:
        job_title = job_block.select_one(job_title_selector)
        job_url = job_block.select_one(job_url_selector)

        if job_title and job_url:
            jobs.append({'Job-title': job_title.get_text(strip=True), 'URL': job_url['href']})

    # Close the WebDriver
    driver.quit()

    # Return JSON response
    return json.dumps(jobs)

if __name__ == "__main__":
    # The target HTML file name should be an argument sent from an external source
    html_file_name = sys.argv[1]
    print(scrape_job_listings(html_file_name))
