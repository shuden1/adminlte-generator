import sys
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import threading
import json

# Assume target_html_file is obtained from the first command line argument.
# In actual implementation, replace the line below with:
# target_html_file = sys.argv[1]
target_html_file = sys.argv[1]

# WebDriver setup
service = Service(executable_path=r"C:\Python3\chromedriver.exe")
options = webdriver.ChromeOptions()
profile_folder_path = "D:\\Mind\\CRA\\AI_Experiments\\Job_Crawlers\\Peter\\adminlte-generator\\chrome_profile\\" + str(threading.get_ident())
options.add_argument(f"user-data-dir={profile_folder_path}")
options.add_argument("--headless")
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")

# Instantiate a WebDriver
driver = webdriver.Chrome(service=service, options=options)

# Open the HTML file
driver.get(f"file:///{target_html_file}")

# Correct selectors based on re-examination of the provided HTML structure
# Assuming job listings are found within div blocks with a specific class, and URLs are in href inside <a> tags under these divs.
# Adjust these selectors based on the actual structure in 'file-QI7mo7s13UOJhFwtNgBePKlh'
job_listings_selector = ".sc-1dywz0m-0 .sc-1qe5ahw-0 .sc-18rtkup-1 .sc-18rtkup-0 tbody tr"
job_title_and_url_selector = "td a"

# Initiate an empty list to hold the job details
jobs = []

# Find all job listing elements using their CSS selector
job_elements = driver.find_elements(By.CSS_SELECTOR, job_listings_selector)

for job_element in job_elements:
    # For each job element, find the <a> tag containing the job title and the URL
    a_element = job_element.find_element(By.CSS_SELECTOR, job_title_and_url_selector)
    job_title = a_element.text  # The text of the <a> element is the job title
    job_url = a_element.get_attribute('href')  # Get the URL from the href attribute
    jobs.append({"Job-title": job_title, "URL": job_url})

# Close the driver
driver.quit()

# Print the jobs in a JSON format
print(json.dumps(jobs))