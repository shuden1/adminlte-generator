from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
import json
import sys
import threading

# The target HTML file name is given as a command-line argument
html_file_path = sys.argv[1]

service = ChromeService(executable_path=r"C:\Python3\chromedriver.exe")
profile_folder_path = "D:\\Mind\\CRA\\AI_Experiments\\Job_Crawlers\\Peter\\adminlte-generator\\chrome_profile\\" + str(threading.get_ident())

options = webdriver.ChromeOptions()
options.add_argument(f"user-data-dir={profile_folder_path}")
options.add_argument("--headless")
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")

driver = webdriver.Chrome(service=service, options=options)

# Open the local HTML file
driver.get(f"file:///{html_file_path}")

# Selectors defined from Step 1 (based on given instructions)
job_blocks_selector = ".card.card-hover"
job_title_selector = "h3 > a"
job_link_attribute = "href"

jobs = []
for job_block in driver.find_elements(By.CSS_SELECTOR, job_blocks_selector):
    job_title = job_block.find_element(By.CSS_SELECTOR, job_title_selector).text
    job_url = job_block.find_element(By.CSS_SELECTOR, job_title_selector).get_attribute(job_link_attribute)
    jobs.append({"Job-title": job_title, "URL": job_url})

print(json.dumps(jobs))

driver.quit()