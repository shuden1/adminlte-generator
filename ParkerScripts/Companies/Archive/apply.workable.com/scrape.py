from selenium import webdriver
import os
from dotenv import load_dotenv

load_dotenv()
from selenium.webdriver.common.by import By
import json
import sys

# Assuming that the job opening blocks can be uniquely identified by the job list class "styles--Qqz1P"
# and each job opening by the list item class "styles--1vo9F"
# Job Titles can be found within "h2.styles--3TJHk" and URLs within "a.styles--1OnOt"

job_openings_selector = ".styles--Qqz1P .styles--1vo9F"
job_title_selector = "h3.styles--3TJHk"
job_url_selector = "a.styles--1OnOt"

# Selenium Script to extract job openings and output to JSON
def main(html_file):
    options = webdriver.ChromeOptions()
    options.add_argument("headless")
    driver = webdriver.Chrome(options=options)
    driver.get(f"file://{html_file}")

    job_listings = driver.find_elements(By.CSS_SELECTOR, job_openings_selector)
    output = []

    for job in job_listings:
        title_element = job.find_element(By.CSS_SELECTOR, job_title_selector)
        link_element = job.find_element(By.CSS_SELECTOR, job_url_selector)
        job_title = title_element.text
        job_url = link_element.get_attribute('href')
        output.append({"Job-title": job_title, "URL": job_url})

    driver.quit()
    print(json.dumps(output))

if __name__ == "__main__":
    html_file_path = sys.argv[1]
    main(html_file_path)
