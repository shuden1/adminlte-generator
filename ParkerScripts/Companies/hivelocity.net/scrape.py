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

# The target HTML file name is provided as a command-line argument
html_file_name = sys.argv[1]

def scrape_job_listings(html_file):
    profile_folder_path = os.getenv("CHROME_PROFILE_PATH") + os.path.sep + str(threading.get_ident())

    service = ChromeService(executable_path=r""+os.getenv("CHROME_DRIVER_PATH")+"")
    options = webdriver.ChromeOptions()
    options.add_argument(f"user-data-dir={profile_folder_path}")
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")

    driver = webdriver.Chrome(service=service, options=options)
    driver.get(f"file:///{html_file}")

    # Selectors for job titles and URLs (based on the structure of the actual job listings section)
    jobs_data = []

    # Get all the job blocks that includes the job title and the URL
    job_blocks = driver.find_elements(By.CSS_SELECTOR, "div[class*='elementor-widget-wrap']")

    for block in job_blocks:
        if block.find_elements(By.CSS_SELECTOR, ".accordion-panel-title h2") and block.find_elements(By.CSS_SELECTOR, ".elementor-button"):
            job_title = block.find_element(By.CSS_SELECTOR, ".accordion-panel-title h2")
            job_link = block.find_element(By.CSS_SELECTOR, ".elementor-button")
            if job_title and job_link:
                title = job_title.text.strip()
                url = job_link.get_attribute("href")
                jobs_data.append({"Job-title": title, "URL": url})

    # Clean up
    driver.quit()


    # Return the JSON data
    return json.dumps(jobs_data)

# Call the function with the HTML file name
print(scrape_job_listings(html_file_name))
