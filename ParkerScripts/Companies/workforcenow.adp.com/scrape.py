import sys
import json
import shutil
import threading
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

# Take the target HTML file name as an argument from the console command
target_html_file = sys.argv[1]

# Initializing a headless webdriver
profile_folder_path = f"D:\\Mind\\CRA\\AI_Experiments\\Job_Crawlers\\Peter\\adminlte-generator\\chrome_profile\\{str(threading.get_ident())}"
service = ChromeService(executable_path=r"C:\Python3\chromedriver.exe")
options = Options()
options.add_argument(f"user-data-dir={profile_folder_path}")
options.add_argument("--headless")
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")

driver = webdriver.Chrome(service=service, options=options)

try:
    # Open the local HTML file
    driver.get(f"file://{target_html_file}")

    # Use the BeautifulSoup's findings to scrape job listings
    job_blocks = driver.find_elements(By.CSS_SELECTOR, "div.current-openings-item")

    # Collecting jobs data
    jobs_data = []
    for job in job_blocks:
        title_elem = job.find_element(By.CSS_SELECTOR, "span.current-opening-title")
        apply_button = job.find_element(By.CSS_SELECTOR, "div.current-openings-apply button")
        job_id = apply_button.get_attribute('id')
        job_title = title_elem.text.strip()
        job_url = f"javascript:openJobDescription('{job_id}')"

        jobs_data.append({"Job-title": job_title, "URL": job_url})

    # Outputting the scraped data as JSON
    print(json.dumps(jobs_data))

finally:
    driver.quit()
