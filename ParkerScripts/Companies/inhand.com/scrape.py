import json
import sys
import shutil
import threading
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

def scrape_jobs(html_file):
    # Set up the Chrome driver and options
    thread_id = threading.get_ident()
    profile_folder_path = f"D:\\Mind\\CRA\\AI_Experiments\\Job_Crawlers\\Peter\\adminlte-generator\\chrome_profile\\{thread_id}"
    options = Options()
    options.add_argument(f"user-data-dir={profile_folder_path}")
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    service = Service(executable_path=r"C:\Python3\chromedriver.exe")

    # Initialize the WebDriver
    driver = webdriver.Chrome(service=service, options=options)
    driver.get(f"file:///{html_file}")

    # Selectors based on the classes found in the provided block
    job_listings = []
    job_blocks = driver.find_elements(By.CSS_SELECTOR, ".elementor-element.hover-toggle")
    for job_block in job_blocks:
        titles = job_block.find_elements(By.CSS_SELECTOR, "a")
        for title in titles:
            job_title = title.text.strip()
            job_url = "https://www.inhand.com/en/company/work-at-inhand/#open-positions"
            if job_title and job_url:
                job_listings.append({"Job-title": job_title, "URL": job_url})

    # Quit the driver and cleanup
    driver.quit()


    # Return the result
    return json.dumps(job_listings)

if __name__ == "__main__":
    html_file = sys.argv[1]
    print(scrape_jobs(html_file))
