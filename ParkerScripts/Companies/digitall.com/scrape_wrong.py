import sys
from selenium import webdriver
import os
from dotenv import load_dotenv

load_dotenv()
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
import threading
import json

# Set up Selenium WebDriver
options = webdriver.ChromeOptions()
profile_folder_path = f"D:\\Mind\\CRA\\AI_Experiments\\Job_Crawlers\\Peter\\adminlte-generator\\chrome_profile\\{threading.get_ident()}"
options.add_argument(f"user-data-dir={profile_folder_path}")
options.add_argument("--headless")
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")
service = ChromeService(executable_path=r""+os.getenv("CHROME_DRIVER_PATH")+"")

driver = webdriver.Chrome(service=service, options=options)

# Load the HTML file. Note: The actual filename will be passed as an argument.
# Use sys.argv[1] in actual script; replace 'your_html_file.html' with sys.argv[1] for dynamic filename input
html_file_name = sys.argv[1]
driver.get(f"file:///{html_file_name}")

# Scrape job titles and URLs based on common HTML structures
# This is a hypothetical selector, replace '.job-opening' and inner selectors with actual ones from your HTML file
job_elements = driver.find_elements(By.CSS_SELECTOR, ".job-opening")
jobs_list = []

for job_element in job properties:
    # Hypothetical selectors for job title and link
    job_title = job_element.find_element(By.CSS_SELECTOR, ".job-title").text
    job_link = job_element.find_element(By.CSS_SELECTOR, "a").get_attribute('href')

    jobs_list.append({"Job-title": job_title, "URL": job_link})

driver.quit()

# Print the list of jobs in JSON format
print(json.dumps(jobs_list))
