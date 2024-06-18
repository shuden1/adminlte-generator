import sys
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
import json
import threading

# The target HTML file name is received as an argument from the console command
target_html_file_name = sys.argv[1]

# Initialize a headless webdriver
service = ChromeService(executable_path=r"C:\Python3\chromedriver.exe")
profile_folder_path = "D:\\Mind\\CRA\\AI_Experiments\\Job_Crawlers\\Peter\\adminlte-generator\\chrome_profile\\" + str(threading.get_ident())
options = webdriver.ChromeOptions()
options.add_argument(f"user-data-dir={profile_folder_path}")
options.add_argument("--headless")
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")

driver = webdriver.Chrome(service=service, options=options)

# Open the target HTML file
driver.get(f"file:///{target_html_file_name}")

# Scrape all job listings using the defined selectors
job_cards = driver.find_elements(By.CSS_SELECTOR, ".job-card")
jobs_list = []

for card in job_cards:
    title_element = card.find_element(By.CSS_SELECTOR, ".job-card__title")
    job_title = title_element.text
    job_url = title_element.get_attribute("href")
    jobs_list.append({"Job-title": job_title, "URL": job_url})

# Close the driver
driver.quit()

# Return scraped data as JSON
print(json.dumps(jobs_list))