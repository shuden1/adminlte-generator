from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
import threading
import shutil
import json
import sys

# Validate parameter entry
if len(sys.argv) != 2:
    print('Please provide the HTML filename as the argument')
    sys.exit(1)

# Get the HTML file name from the external console command
html_filename = sys.argv[1]

# Initialise a headless webdriver
profile_folder_path = "D:\\Mind\\CRA\\AI_Experiments\\Job_Crawlers\\Peter\\adminlte-generator\\chrome_profile\\" + str(threading.get_ident())
service = ChromeService(executable_path=r"C:\Python3\chromedriver.exe")
options = webdriver.ChromeOptions()
options.add_argument(f"user-data-dir={profile_folder_path}")
options.add_argument("--headless")
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")

# Create the webdriver
driver = webdriver.Chrome(service=service, options=options)

# Open the local HTML file
driver.get(f"file:///{html_filename}")

# Use the selectors identified in Step 1 to scrape job listings
job_elements = driver.find_elements(By.CSS_SELECTOR, ".career-page-list-item")
job_listings = []

# Loop through job elements found and extract the job titles and associated URLs
for job_element in job_elements:
    title_element = job_element.find_element(By.CSS_SELECTOR, ".career-page-list-item-title")
    link_element = job_element.find_element(By.CSS_SELECTOR, "a.ct-link-button.dark-btn")
    job_title = title_element.text.strip()
    job_url = link_element.get_attribute("href")
    job_listings.append({"Job-title": job_title, "URL": job_url})

# Clean up and remove the profile folder
driver.quit()


# Print the result as a JSON string
print(json.dumps(job_listings))
