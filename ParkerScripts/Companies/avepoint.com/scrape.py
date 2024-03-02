import json
import shutil
import sys
import threading
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By

# Step 1: Identifying the selectors for job titles and URLs
# The block with job openings is within a <dl> element with a class of 'open-positions'
job_opening_block_selector = ".open-positions"
# Job titles are in <a> elements, with the job title being the text of a <span> without a class
job_title_selector = "dd a span:nth-of-type(1)"
# The URL is the 'href' attribute of the <a> element
job_url_selector = "dd a"

# Step 2: Creating the Python + Selenium script
# The target HTML file name should be an argument sent from an external source through the console command
html_file_name = sys.argv[1]

# Initialise a headless webdriver
profile_folder_path = "D:\\Mind\\CRA\\AI_Experiments\\Job_Crawlers\\Peter\\adminlte-generator\\chrome_profile\\" + str(threading.get_ident())
service = Service(executable_path=r"C:\Python3\chromedriver.exe")
options = webdriver.ChromeOptions()
options.add_argument(f"user-data-dir={profile_folder_path}")
options.add_argument("--headless")
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")

# Create a new driver instance
driver = webdriver.Chrome(service=service, options=options)

# Open the HTML file
driver.get(f"file:///{html_file_name}")

# Scrape all job listings using the selectors defined in Step 1
job_elements = driver.find_elements(By.CSS_SELECTOR, job_opening_block_selector + ' ' + job_url_selector)
job_listings = []
for job_element in job_elements:
    job_title = job_element.find_element(By.CSS_SELECTOR, job_title_selector).get_attribute('textContent').strip()
    job_url = job_element.get_attribute('href').strip()
    if job_title.startswith('Position: '):
        job_title = job_title.split('Position: ')[1]
    job_listings.append({"Job-title": job_title, "URL": job_url})

# Return a JSON
json_result = json.dumps(job_listings)
print(json_result)

# Close the Webdriver
driver.quit()

# Remove the user profile directory
