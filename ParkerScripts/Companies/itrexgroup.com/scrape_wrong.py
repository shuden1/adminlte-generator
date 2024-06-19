import sys
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
import threading
import json

# The target HTML file name comes from the command line argument
target_html_file = sys.argv[1]

profile_folder_path = "D:\\Mind\\CRA\\AI_Experiments\\Job_Crawlers\\Peter\\adminlte-generator\\chrome_profile\\" + str(threading.get_ident())
service = ChromeService(executable_path=r"C:\Python3\chromedriver.exe")
options = webdriver.ChromeOptions()
options.add_argument(f"user-data-dir={profile_folder_path}")
options.add_argument("--headless")
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")

driver = webdriver.Chrome(service=service, options=options)

# Since we're going to work with a local file, use the file protocol
url = f"file:///{target_html_file}"
driver.get(url)

jobs_list = []

# Initial attempt with incorrect selectors, providing a new approach
# Assuming the corrected HTML analysis led to these selectors
job_elements = driver.find_elements(By.CSS_SELECTOR, "article")
for job_element in job_elements:
    title = job_element.find_element(By.TAG_NAME, "h2").text  # Assuming job titles are in <h2> tags
    url = job_element.find_element(By.TAG_NAME, "a").get_attribute('href')  # Assuming URL is within an <a> tag in each article
    if title and url:  # Ensure both title and url contain values
        jobs_list.append({"Job-title": title, "URL": url})

driver.quit()

# Converting the list into JSON format and displaying it
print(json.dumps(jobs_list))