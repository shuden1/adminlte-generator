import json
import shutil
import sys
import threading
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

# Step 1 analysis should give the following accurate selectors (these are placeholders):
job_block_selector = ".job-opening"  # Placeholder class for job blocks
job_title_selector = "h3 > a"        # Placeholder selector for job titles within job blocks

if __name__ == "__main__":
    html_file_name = sys.argv[1]   # Filename from the external source as an argument

    profile_folder_path = "D:\\Mind\\CRA\\AI_Experiments\\Job_Crawlers\\Peter\\adminlte-generator\\chrome_profile\\" + str(threading.get_ident())

    options = Options()
    options.headless = True
    options.add_argument(f"user-data-dir={profile_folder_path}")

    service = Service(executable_path=r"C:\Python3\chromedriver.exe")

    driver = webdriver.Chrome(service=service, options=options)
    driver.get(f"file://{html_file_name}")

    job_listings = []
    job_elements = driver.find_elements(By.CSS_SELECTOR, job_block_selector)

    for job_element in job_elements:
        job_title_elem = job_element.find_elements(By.CSS_SELECTOR, job_title_selector)
        for title_elem in job_title_elem:
            job_title = title_elem.text
            job_url = title_elem.get_attribute('href')
            job_listings.append({"Job-title": job_title, "URL": job_url})

    print(json.dumps(job_listings))

    driver.quit()
