from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import threading
import sys
import json

# Accepting target HTML file name from the console argument
target_html_file = sys.argv[1]

# Set up ChromeDriver options and service
options = Options()
profile_folder_path = "D:\\Mind\\CRA\\AI_Experiments\\Job_Crawlers\\Peter\\adminlte-generator\\chrome_profile\\" + str(threading.get_ident())
options.add_argument(f"user-data-dir={profile_folder_path}")
options.add_argument("--headless")
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")
service = ChromeService(executable_path=r"C:\Python3\chromedriver.exe")

# Initialize WebDriver
driver = webdriver.Chrome(options=options, service=service)

# Open the given HTML file
driver.get(f"file:///{target_html_file}")

# Selectors identified in Step 1
job_blocks_selector = ".css-1q2dra3"
job_title_selector = ".css-19uc56f"
job_url_selector = ".css-19uc56f"

# Scrape job listings
job_listings = []
job_elements = driver.find_elements(By.CSS_SELECTOR, job_blocks_selector)
for job_element in job_elements:
    title_element = job_element.find_element(By.CSS_SELECTOR, job_title_selector)
    job_title = title_element.text
    job_url = title_element.get_attribute("href")
    job_listings.append({"Job-title": job_title, "URL": job_url})

# Return scraped data as JSON
print(json.dumps(job_listings))

# Close the driver
driver.quit()