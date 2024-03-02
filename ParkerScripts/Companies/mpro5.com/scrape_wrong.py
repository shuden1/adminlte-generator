import sys
import threading
import shutil
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import NoSuchElementException

# The target HTML file is passed as an argument from the console command
html_file_name = sys.argv[1]

profile_folder_path = "D:\\Mind\\CRA\\AI_Experiments\\Job_Crawlers\\Peter\\adminlte-generator\\chrome_profile\\"+str(threading.get_ident())

options = webdriver.ChromeOptions()
options.add_argument(f"user-data-dir={profile_folder_path}")
options.add_argument("--headless")
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")

service = Service(executable_path=r"C:\Python3\chromedriver.exe")

driver = webdriver.Chrome(service=service, options=options)
driver.get(f"file://{html_file_name}")

try:
    # Step 1: Identifying the exact HTML selectors
    job_blocks_selector = ".row-fluid-wrapper.row-depth-1.row-number-7 .span12.widget-span.widget-type-custom_widget.dnd-module"
    job_title_selector = "h2 span[dir='ltr']"

    # Step 2: Scraping the Job Titles and URLs
    job_blocks = driver.find_elements(By.CSS_SELECTOR, job_blocks_selector)
    job_listings = []

    for block in job_blocks:
        try:
            job_title_element = block.find_element(By.CSS_SELECTOR, job_title_selector)
            apply_button_element = block.find_element(By.XPATH, ".//a[contains(text(), 'Apply For Job')]")
            job_title = job_title_element.text.strip()
            job_url = apply_button_element.get_attribute('href')
            job_listings.append({"Job-title": job_title, "URL": job_url})
        except NoSuchElementException:
            # If either Job Title or the Apply button with Job URL is not found, skip the current iteration
            continue

    # Print the result as a JSON
    print(job_listings)

finally:
    driver.quit()
