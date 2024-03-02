import threading
import shutil
import json
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import sys

# Step 1: Selectors
job_block_selector = ".job-list-section .job-item"
job_title_selector = "h3"
job_url_selector = "div.button a"

# Step 2: Python + Selenium script
def scrape_job_listings(html_file_path):
    profile_folder_path = "D:\\Mind\\CRA\\AI_Experiments\\Job_Crawlers\\Peter\\adminlte-generator\\chrome_profile\\" + str(threading.get_ident())
    service = ChromeService(executable_path=r"C:\Python3\chromedriver.exe")

    options = Options()
    options.add_argument(f"user-data-dir={profile_folder_path}")
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")

    driver = webdriver.Chrome(service=service, options=options)

    # Open the local HTML file
    driver.get(f"file://{html_file_path}")

    # Scrape job listings
    jobs_data = []
    job_blocks = driver.find_elements(by=By.CSS_SELECTOR, value=job_block_selector)
    for job_block in job_blocks:
        title_element = job_block.find_element(by=By.CSS_SELECTOR, value=job_title_selector)
        url_element = job_block.find_element(by=By.CSS_SELECTOR, value=job_url_selector)
        jobs_data.append({
            "Job-title": title_element.text,
            "URL": url_element.get_attribute("href")
        })

    driver.quit()

    # Remove the profile folder


    # Return JSON data
    return json.dumps(jobs_data, indent=2)

# Calling the function with the file path from argument if this script is run as main
if __name__ == '__main__':
    path_to_html_file = sys.argv[1]
    print(scrape_job_listings(path_to_html_file))
