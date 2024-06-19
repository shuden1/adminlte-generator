import sys
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
import json
import threading

# Setup ChromeDriver (correct the service instantiation and typo)
service = Service(executable_path=r"C:\Python3\chromedriver.exe")
options = webdriver.ChromeOptions()
profile_folder_path = "D:\\Mind\\CRA\\AI_Experiments\\Job_Crawlers\\Peter\\adminlte-generator\\chrome_profile\\" + str(threading.get_ident())
options.add_argument(f"user-data-dir={profile_folder_path}")
options.add_argument("--headless")
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")

# Initialize WebDriver with the defined service and options
driver = webdriver.Chrome(service=service, options=options)

# Assuming the first argument passed to the script is the target HTML file name
target_html_file = sys.argv[1]

# Open the target HTML file
driver.get(f"file:///{target_html_file}")

# Define CSS selectors for job titles and URLs
job_elements_selector = ".jobItemList .jobItemContent a[href]"
job_elements = driver.find_elements(By.CSS_SELECTOR, job_elements_selector)

# Extract job titles and URLs
jobs = [{"Job-title": e.text, "URL": e.get_attribute("href")} for e in job_elements]

# Print the result as JSON
print(json.dumps(jobs))

# Quit the driver session
driver.quit()