from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
import sys
import json

# Retrieve target HTML file name from command line argument
target_html_file_name = sys.argv[1]

# Initialize WebDriver
profile_folder_path = "D:\\Mind\\CRA\\AI_Experiments\\Job_Crawlers\\Peter\\adminlte-generator\\chrome_profile\\" + str(threading.get_ident())
options = webdriver.ChromeOptions()
options.add_argument(f"user-data-dir={profile_folder_path}")
options.add_argument("--headless")
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")
service = ChromeService(executable_path=r"C:\Python3\chromedriver.exe")
driver = webdriver.Chrome(options=options, service=service)

driver.get(f"file://{html_file_name}")

# Read the content of the file using BeautifulSoup
soup = BeautifulSoup(driver.page_source, 'html.parser')

# Find job opening blocks and job titles with URLs
job_opening_selectors = {
    "blocks": "div.opening",
    "title": "a[data-mapped='true']"
}

job_listings = []
for job_block in soup.select(job_opening_selectors["blocks"]):
    job_title_tag = job_block.select_one(job_opening_selectors["title"])
    if job_title_tag:
        job_title = job_title_tag.text.strip()
        job_url = job_title_tag['href'].strip()
        job_listings.append({"Job-title": job_title, "URL": job_url})

driver.quit()

# Print the result in JSON format
print(json.dumps(job_listings))
