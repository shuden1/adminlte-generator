from bs4 import BeautifulSoup
import sys
from selenium import webdriver
import os
from dotenv import load_dotenv

load_dotenv()
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
import threading
import shutil
import json

# Extract the filename from the command line argument
filename = sys.argv[1]

# Read the HTML file
with open(filename, 'r', encoding='utf-8') as file:
    html_content = file.read()

# Parse the HTML content using BeautifulSoup
soup = BeautifulSoup(html_content, 'html.parser')

# Define the Empty dictionary to store Job Openings selectors.
job_opening_selectors = {}
job_titles_and_urls_selectors = []

# Extract the blocks containing Job Openings
jobs_list = soup.select("ul.list-group")
for jobs in jobs_list:
    job_items = jobs.select('li.list-group-item')
    for job in job_items:
        title = job.select_one('h4 > a').text.strip()
        link = job.select_one('h4 > a')['href'].strip()
        job_selectors = {'Job-title': title, 'URL': link}
        job_titles_and_urls_selectors.append(job_selectors)

# If no ul.list-group found, search for div blocks that might contain job openings
if len(job_titles_and_urls_selectors) == 0:
    job_blocks = soup.find_all('div', class_=lambda value: value and value.startswith('jobs'))
    for block in job_blocks:
        anchors = block.find_all('a')
        for a in anchors:
            if a.find_parent('h') is not None:
                title = a.text.strip()
                link = a['href'].strip()
                job_selectors = {'Job-title': title, 'URL': link}
                job_titles_and_urls_selectors.append(job_selectors)

# Define the selectors for real scraping with Selenium step.
job_opening_selectors["blocks"] = "ul.list-group > li.list-group-item"
job_opening_selectors["title"] = "h4 > a"

# Selenium Step:
def scrape_job_listings():
    profile_folder_path = os.getenv("CHROME_PROFILE_PATH") + "\\" + str(threading.get_ident())
    service = ChromeService(executable_path=r""+os.getenv("CHROME_DRIVER_PATH")+"")
    options = webdriver.ChromeOptions()
    options.add_argument(f"user-data-dir={profile_folder_path}")
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")

    driver = webdriver.Chrome(service=service, options=options)
    driver.get('file://' + filename)

    job_blocks_selector = job_opening_selectors.get("blocks", "")
    job_title_and_url_selector = job_opening_selectors.get("title", "")

    job_listings = []
    job_elements = driver.find_elements(by=By.CSS_SELECTOR, value=job_blocks_selector)
    for job_element in job_elements:
        title_element = job_element.find_element(By.CSS_SELECTOR, value=job_title_and_url_selector)
        title = title_element.text
        url = title_element.get_attribute('href')
        job_listings.append({"Job-title": title, "URL": url})

    driver.quit()

    # Remove the profile folder after scraping


    # Return the scraped data as JSON
    return json.dumps(job_listings)

# Call the function and print the result
print(scrape_job_listings())
