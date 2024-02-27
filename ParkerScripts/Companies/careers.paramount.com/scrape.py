import sys
import threading
import shutil
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
import json

# Step 2: Selenium script
def scrape_job_listings(html_file_name):
    # ChromeDriver configuration
    options = webdriver.ChromeOptions()
    profile_folder_path = f"D:\\Mind\\CRA\\AI_Experiments\\Job_Crawlers\\Peter\\adminlte-generator\\chrome_profile\\{threading.get_ident()}"
    options.add_argument(f"user-data-dir={profile_folder_path}")
    options.add_argument("--headless")
    service = ChromeService(executable_path=r"C:\Python3\chromedriver.exe")

    driver = webdriver.Chrome(service=service, options=options)

    driver.get(f"file:///{html_file_name}")

    # Scraping job listings
    jobs = []
    for job_block in driver.find_elements(By.CSS_SELECTOR, ".job-tile"):
        title_element = job_block.find_element(By.CSS_SELECTOR, ".tiletitle a.jobTitle-link")
        job_title = title_element.text.strip()
        job_url = title_element.get_attribute('href').strip()
        jobs.append({"Job-title": job_title, "URL": job_url})

    driver.quit()
    shutil.rmtree(profile_folder_path)
    
    return json.dumps(jobs)

# The actual command-line argument would be taken from sys.argv[1], but for this example, we'll set it manually
html_file_name = sys.argv[1]
print(scrape_job_listings(html_file_name))