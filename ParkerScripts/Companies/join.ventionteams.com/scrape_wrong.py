from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
import json
import sys
import threading

# Retrieve the target HTML file name from the command line argument
target_html_file = sys.argv[1]

# Configure Selenium with Chrome options
service = ChromeService(executable_path=r"C:\Python3\chromedriver.exe")
options = webdriver.ChromeOptions()
profile_folder_path = "D:\\Mind\\CRA\\AI_Experiments\\Job_Crawlers\\Peter\\adminlte-generator\\chrome_profile\\" + str(threading.get_ident())
options.add_argument(f"user-data-dir={profile_folder_path}")
options.add_argument("--headless")
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")

# Initialise WebDriver
driver = webdriver.Chrome(service=service, options=options)

# Open the target HTML file
driver.get(f"file:///{target_html_file}")

# Extract Job Listings
job_listings = []
elements = driver.find_elements(By.CSS_SELECTOR, ".css-bz3ry3")
for element in elements:
    job_url = element.find_element(By.TAG_NAME, "a").get_attribute('href')
    job_title = element.find_element(By.CSS_SELECTOR, ".css-prn0qn").text
    if job_title:  # Check if job title is not empty
        job_listings.append({"Job-title": job_title, "URL": job_url})

# Format and print job listings as JSON
print(json.dumps(job_listings, ensure_ascii=False))

driver.quit()