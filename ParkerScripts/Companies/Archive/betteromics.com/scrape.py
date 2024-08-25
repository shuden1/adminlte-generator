from selenium import webdriver
import os
from dotenv import load_dotenv

load_dotenv()
from selenium.webdriver.common.by import By
import sys
import json

def scrape_job_listings(html_file):
    # Initialize the driver
    driver = webdriver.Chrome()

    # Open the local HTML file
    driver.get("file://" + html_file)

    # Find the job opening blocks and extract job titles and associated URLs
    job_openings = []
    job_blocks = driver.find_elements(By.CSS_SELECTOR, ".opening")
    for job in job_blocks:
        title_elements = job.find_elements(By.CSS_SELECTOR, "a[data-mapped='true']")
        for title_element in title_elements:
            title = title_element.text.strip()
            url = title_element.get_attribute('href').strip()
            job_openings.append({"Job-title": title, "URL": url})

    # Close the driver
    driver.quit()

    # Return the job listings in JSON format
    return json.dumps(job_openings, indent=2)


if __name__ == '__main__':
    # The target HTML file name comes from an argument passed through the console command
    html_file_name = sys.argv[1]
    print(scrape_job_listings(html_file_name))
