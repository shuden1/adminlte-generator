from selenium import webdriver
import os
from dotenv import load_dotenv

load_dotenv()
from selenium.webdriver.common.by import By
import json
import sys

def main():
    html_file_path = sys.argv[1]
    driver = webdriver.Chrome()
    driver.get(f"file://{html_file_path}")
    job_elements = driver.find_elements(By.CSS_SELECTOR, '.list-group-item')

    job_data = [{"Job-title": elem.find_element(By.CSS_SELECTOR, 'h4 a').text, "URL": elem.find_element(By.CSS_SELECTOR, 'h4 a').get_attribute('href')} for elem in job_elements]

    driver.quit()

    print(json.dumps(job_data))

if __name__ == "__main__":
    main()
