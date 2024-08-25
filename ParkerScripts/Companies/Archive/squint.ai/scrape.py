from bs4 import BeautifulSoup
import sys
from selenium import webdriver
import os
from dotenv import load_dotenv

load_dotenv()
import json

# Read the HTML content from the file passed as an argument
input_file = sys.argv[1]
with open(input_file, 'r', encoding='utf-8') as file:
    html_content = file.read()

# Using BeautifulSoup to parse HTML content
soup = BeautifulSoup(html_content, 'html.parser')

# Find the job openings blocks
job_blocks = soup.select('.angellist_jobs-job')

# Collect job titles and URLs
job_listings = []
for job_block in job_blocks:
    job_title = job_block.select_one('.angellist_jobs-title-link').get_text(strip=True)
    job_url = job_block.select_one('.angellist_jobs-title-link')['href']
    job_listings.append({"Job-title": job_title, "URL": job_url})

# JSON output
json_output = json.dumps(job_listings)
print(json_output)

# Using Selenium to interact with the web elements
options = webdriver.ChromeOptions()
options.add_argument('headless')

# Assume that the ChromeDriver executable is located in the system's PATH
driver = webdriver.Chrome(options=options)

# driver.get("path_to_local_html_file") # Replace with actual URL or local path
# ^ Since we cannot test or interact with the given HTML file via Selenium in this environment, this part is left incomplete.
