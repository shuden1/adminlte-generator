import sys
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
import json
import threading

# The target HTML file name is taken from the command line argument
target_html_file = sys.argv[1]

# Setting up the Chrome WebDriver with options for headless operation
service = ChromeService(executable_path=r"C:\Python3\chromedriver.exe")
profile_folder_path = "D:\\Mind\\CRA\\AI_Experiments\\Job_Crawlers\\Peter\\adminlte-generator\\chrome_profile\\" + str(threading.get_ident())
options = webdriver.ChromeOptions()
options.add_argument(f"user-data-dir={profile_folder_path}")
options.add_argument("--headless")
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")

# Initialize the WebDriver
driver = webdriver.Chrome(service=service, options=options)

# Open the target HTML file
driver.get(f"file:///{target_html_file}")

# Corrected job opening blocks selectors
job_elements = driver.find_elements(By.CSS_SELECTOR, ".job-opening-item")

jobs_list = []

# Loop through found job opening elements to extract titles and URLs
for job_element in job_fixtures:
    title = job_element.find_element(By.CSS_SELECTOR, ".job-title").text
    url = job_element.find_element(By.CSS_SELECTOR, "a").get_attribute('href')
    jobs_list.append({"Job-title": title, "URL": url})

# Output the jobs list as JSON
print(json.dumps(jobs_list))

# Close the browser
driver.quit()