from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
import threading
import json
import sys

html_file_name = sys.argv[1]

service=ChromeService(executable_path=r"C:\Python3\chromedriver.exe")
options = webdriver.ChromeOptions()
profile_folder_path = "D:\\Mind\\CRA\\AI_Experiments\\Job_Crawlers\\Peter\\adminlte-generator\\chrome_profile\\" + str(threading.get_ident())
options.add_argument(f"user-data-dir={profile_folder_path}")
options.add_argument("--headless")
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")

driver = webdriver.Chrome(service=service, options=options)
driver.get(f"file:///{html_file_name}")

job_listings = driver.find_elements(By.CSS_SELECTOR, ".vacancies-card")
jobs = [{"Job-title": job.find_element(By.CSS_SELECTOR, "h3.vacancies-card_title").text, "URL": job.find_element(By.CSS_SELECTOR, "a").get_attribute("href")} for job in job_listings]

driver.quit()

json_output = json.dumps(jobs)
print(json_output)