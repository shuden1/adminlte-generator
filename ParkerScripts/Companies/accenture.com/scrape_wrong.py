import sys
import threading
from selenium import webdriver
import os
from dotenv import load_dotenv

load_dotenv()
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service

def main(target_html_file):
    profile_folder_path = os.getenv("CHROME_PROFILE_PATH") + "\\" + str(threading.get_ident())
    service = Service(executable_path=r""+os.getenv("CHROME_DRIVER_PATH")+"")
    options = webdriver.ChromeOptions()
    options.add_argument(f"user-data-dir={profile_folder_path}")
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")

    driver = webdriver.Chrome(service=service, options=options)
    driver.get(f"file:///{target_html_file}")

    job_listings = []
    # Assuming job_block_selector, job_title_selector, and job_url_selector are identified in Step 1
    job_blocks = driver.find_elements(By.CSS_SELECTOR, ".job-opening")
    for job_block in job_blocks:
        title_elements = job_block.find_elements(By.CSS_SELECTOR, "h3 a")
        for title_element in title_elements:
            job_title = title_element.text
            job_url = title_element.get_attribute('href')
            job_listings.append({"Job-title": job_title, "URL": job_url})

    driver.quit()
    print(job_listings)

if __name__ == "__main__":
    main(sys.argv[1])
