import sys
from selenium import webdriver
from selenium.webdriver.common.by import By
import threading
import json

# Assuming the command line argument is properly passed, retrieve the HTML file name
html_file_name = sys.argv[1]

profile_folder_path="D:\\Mind\\CRA\\AI_Experiments\\Job_Crawlers\\Peter\\adminlte-generator\\chrome_profile\\"+str(threading.get_ident())

options = webdriver.ChromeOptions()
options.add_argument(f"user-data-dir={profile_folder_path}")
options.add_argument("--headless")
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")

service = webdriver.chrome.service.Service(executable_path=r"C:\Python3\chromedriver.exe")
driver = webdriver.Chrome(service=service, options=options)

driver.get(f"file://{html_file_name}")

elements = driver.find_elements(By.CSS_SELECTOR, ".vacancy-item")

jobs = [{"Job-title": element.find_element(By.CSS_SELECTOR, ".vacancy__title").text, 
         "URL": element.find_element(By.CSS_SELECTOR, "a").get_attribute("href")} for element in elements]

print(json.dumps(jobs))