import sys
from selenium import webdriver
import threading
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
import json

# Fetching the file name from the external source through console command as the single input to the script
target_html_file_name = sys.argv[1]

# Setting the profile folder path for Chrome
profile_folder_path = "D:\\Mind\\CRA\\AI_Experiments\\Job_Crawlers\\Peter\\adminlte-generator\\chrome_profile\\" + str(threading.get_ident())

# Configuring ChromeDriver options
options = webdriver.ChromeOptions()
options.add_argument(f"user-data-dir={profile_folder_path}")
options.add_argument("--headless")
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")

# Setting the ChromeDriver service
service = ChromeService(executable_path=r"C:\Python3\chromedriver.exe")

# Initializing the WebDriver with the specified service and options
driver = webdriver.Chrome(service=service, options=options)

# Opening the target HTML page
driver.get(f"file:///{target_html_file_name}")

# Scraping the job elements using the corrected selectors
job_elements = driver.find_elements(By.CSS_SELECTOR, ".vacancies--vacancy-card")

jobs = []
for element in job_elements:
    title_element = element.find_element(By.CSS_SELECTOR, ".vacancy-title")
    job_title = title_element.text 
    job_url = element.get_attribute('href')
    jobs.append({"Job-title": job_title, "URL": job_url})

driver.quit()

# Printing the results in the required format (as a JSON string for clarity)
print(json.dumps(jobs))