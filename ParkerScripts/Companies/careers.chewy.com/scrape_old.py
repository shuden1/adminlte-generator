import json
import shutil
import sys
import threading
from selenium import webdriver
import os
from dotenv import load_dotenv

load_dotenv()
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By

# Step 1 result from BeautifulSoup (Assume this is the correct one from simulation)
job_block_selector = '.jobs-list-item'  # Placeholder selector for job blocks
job_title_selector = '.job-title'  # Placeholder selector for job titles within job blocks
job_url_selector = 'a'  # Placeholder selector for job URLs within job blocks

# Step 2: actual Python + Selenium script

def scrape_job_listings(html_file_name):
    # Profile path setup
    profile_path = f"D:\\Mind\\CRA\\AI_Experiments\\Job_Crawlers\\Peter\\adminlte-generator\\chrome_profile\\{threading.get_ident()}"

    options = webdriver.ChromeOptions()
    options.add_argument(f"user-data-dir={profile_path}")
    options.add_argument("--headless")

    # Set ChromeDriver service
    service = ChromeService(executable_path=r""+os.getenv("CHROME_DRIVER_PATH")+"")

    # Start headless WebDriver
    driver = webdriver.Chrome(service=service, options=options)
    driver.get(f"file:///{html_file_name}")

    # Scrape job listings using defined selectors
    job_listings = []
    job_blocks = driver.find_elements(By.CSS_SELECTOR, job_block_selector)
    for job_block in job_blocks:
        title_element = job_block.find_element(By.CSS_SELECTOR, job_title_selector)
        url_element = job_block.find_element(By.CSS_SELECTOR, job_url_selector)
        job_listings.append({"Job-title": title_element.text, "URL": url_element.get_attribute('href')})

    # Close WebDriver and clean up profile folder
    driver.quit()
    # shutil.rmtree(profile_path)

    # Output job listings as JSON
    return json.dumps(job_listings)

if __name__ == '__main__':
    # HTML file name is the first argument from the command line
    html_file_name = sys.argv[1]
    print(scrape_job_listings(html_file_name))
