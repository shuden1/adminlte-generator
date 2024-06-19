import sys
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
import threading
import json

# The target HTML filename is provided as an argument from an external source
target_html_file = sys.argv[1]

# Setup for headless ChromeDriver with specified profile path
profile_folder_path = "D:\\Mind\\CRA\\AI_Experiments\\Job_Crawlers\\Peter\\adminlte-generator\\chrome_profile\\" + str(threading.get_ident())
service = ChromeService(executable_path=r"C:\Python3\chromedriver.exe")
options = webdriver.ChromeOptions()
options.add_argument(f"user-data-dir={profile_folder_path}")
options.add_argument("--headless")
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")

# Initialize the webdriver
driver = webdriver.Chrome(service=service, options=options)

# Open the target HTML file
driver.get(f"file:///{target_html_file}")

# Scrape all job listings using the correct selectors
job_listings = []
# Use a corrected approach for finding job elements
job_elements = driver.find_elements(By.CSS_SELECTOR, "selector_for_job_title_links")  # Placeholder for correct CSS selector
for job_element in job_elements:
    job_title = job_element.text  # Assuming job title is the text of the link
    job_url = job_element.get_attribute('href')  # Getting the URL from the href attribute
    job_listings.append({"Job-title": job_title, "URL": job_url})

# Close the driver
driver.quit()

# Output the results as JSON, ensuring the list is properly formatted
print(json.dumps(job_listings, ensure_ascii=False))