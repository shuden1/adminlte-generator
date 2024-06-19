import sys
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
import threading
import json

# Target HTML file name received as an argument from the console command
target_html_file_name = sys.argv[1]

# Initialising a headless WebDriver
profile_folder_path = "D:\\Mind\\CRA\\AI_Experiments\\Job_Crawlers\\Peter\\adminlte-generator\\chrome_profile\\" + str(threading.get_ident())
service = ChromeService(executable_path=r"C:\Python3\chromedriver.exe")
options = webdriver.ChromeOptions()
options.add_argument(f"user-data-dir={profile_folder_path}")
options.add_argument("--headless")
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")

driver = webdriver.Chrome(service=service, options=options)

# Opening the target HTML file
driver.get(f"file:///{target_html_file_name}")

# Using the selectors defined in STEP 1 to scrape all job listings
job_listings = []
for element in driver.find_elements(By.CSS_SELECTOR, ".card-hover"):
    title_element = element.find_element(By.CSS_SELECTOR, "h3 a")
    job_title = title_element.text
    job_url = title_element.get_attribute('href')
    job_listings.append({"Job-title": job_title, "URL": job_url})

driver.quit()

# Returning a JSON of scraped job listings
print(json.dumps(job_listings))