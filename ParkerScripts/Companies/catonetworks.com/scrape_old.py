import shutil
import sys
import threading
from selenium import webdriver
import os
from dotenv import load_dotenv

load_dotenv()
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

# The target HTML file name is an argument sent from an external source through the console command
target_html_file = sys.argv[1]

# Step 1 Selectors
job_block_selector = ".b-team-image-gallery--page-careers .gallery-container"
job_title_selector = ".b-team-image-gallery--page-careers .gallery-container h2"
job_url_selector = ".b-team-image-gallery--page-careers .gallery-container .button a"

# Initialise a headless webdriver with the given profile folder path
profile_folder_path = os.getenv("CHROME_PROFILE_PATH") + os.path.sep + str(threading.get_ident())
service = ChromeService(executable_path=r""+os.getenv("CHROME_DRIVER_PATH")+"")
options = Options()
options.add_argument(f"user-data-dir={profile_folder_path}")
options.add_argument("--headless")
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")

driver = webdriver.Chrome(service=service, options=options)

# Scrape all job listings using the selectors
try:
    driver.get(f"file://{target_html_file}")
    job_blocks = driver.find_elements(By.CSS_SELECTOR, job_block_selector)
    jobs_json = []

    for block in job_blocks:
        title_element = block.find_element(By.CSS_SELECTOR, job_title_selector)
        url_element = block.find_element(By.CSS_SELECTOR, job_url_selector)
        job_title = title_element.text
        job_url = url_element.get_attribute('href')
        jobs_json.append({"Job-title": job_title, "URL": job_url})

    print(jobs_json)
finally:
    driver.quit()
