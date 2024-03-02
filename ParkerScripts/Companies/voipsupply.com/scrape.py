from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import sys
import json
import threading
import shutil
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Collect file name from command line argument
html_file = sys.argv[1]

# Set up Chrome options
options = Options()
profile_folder_path = "D:\\Mind\\CRA\\AI_Experiments\\Job_Crawlers\\Peter\\adminlte-generator\\chrome_profile\\" + str(threading.get_ident())
options.add_argument(f"user-data-dir={profile_folder_path}")
options.add_argument("--headless")
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")

# Set up Chrome service
service = ChromeService(executable_path=r"C:\Python3\chromedriver.exe")

# Initialize Chrome webdriver
driver = webdriver.Chrome(service=service, options=options)

# Load the HTML file
driver.get(f"file:///{html_file}")

# Wait until the page and the required elements are loaded
wait = WebDriverWait(driver, 10)
wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".avail-positions-container")))

# Extract job titles and URLs
job_listings = []
for job_block in driver.find_elements(By.CSS_SELECTOR, "ul > ul > ul > li"):
    job_title = job_block.find_element(By.CSS_SELECTOR, "strong > a").text
    job_url = job_block.find_element(By.CSS_SELECTOR, "strong > a").get_attribute('href')
    job_listings.append({"Job-title": job_title, "URL": job_url})

# Output the result as JSON
print(json.dumps(job_listings))

# Close the driver
driver.quit()

# Remove the profile folder

