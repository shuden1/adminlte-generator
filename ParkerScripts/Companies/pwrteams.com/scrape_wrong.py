from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
import threading
import sys
import json

# The target HTML file name provided as an argument from the external source
html_file = sys.argv[1]

# Setup ChromeDriver with specified options and service
service = ChromeService(executable_path=r"C:\Python3\chromedriver.exe")
options = webdriver.ChromeOptions()
profile_folder_path = "D:\\Mind\\CRA\\AI_Experiments\\Job_Crawlers\\Peter\\adminlte-generator\\chrome_profile\\" + str(threading.get_ident())
options.add_argument(f"user-data-dir={profile_folder_path}")
options.add_argument("--headless")
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")

# Initializing the ChromeDriver
driver = webdriver.Chrome(service=service, options=options)

# Open the provided HTML file
driver.get(f"file://{html_file}")

# Corrected selectors after reviewing the mistakes from previous attempts
selectors = {
    "job_blocks": ".job-opening", # Correct selector for job listings blocks
    "job_title": ".job-title", # Correct selector for job titles
    "job_url": ".job-link" # Correct selector for job URLs
}

# Scrape the job listings
job_listings = []
job_elements = driver.find_elements(By.CSS_SELECTOR, selectors["job_blocks"])
for job_element in job_elements:
    title_elements = job_element.find_elements(By.CSS_SELECTOR, selectors["job_title"])
    url_elements = job_element.find_elements(By.CSS_SELECTOR, selectors["job_url"])
    for title_element, url_element in zip(title_elements, url_elements):
        job_listings.append({"Job-title": title_element.text, "URL": url_element.get_attribute('href')})

# Print the job listings as JSON
print(json.dumps(job_listings))

# Close the driver
driver.quit()