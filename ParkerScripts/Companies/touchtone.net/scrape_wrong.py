import sys
import threading
import json
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
import shutil

def scrape_job_listings(html_file):
    profile_folder_path = "D:\\Mind\\CRA\\AI_Experiments\\Job_Crawlers\\Peter\\adminlte-generator\\chrome_profile\\" + str(threading.get_ident())
    service = ChromeService(executable_path=r"C:\Python3\chromedriver.exe")
    options = webdriver.ChromeOptions()
    options.add_argument(f"user-data-dir={profile_folder_path}")
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")

    with webdriver.Chrome(service=service, options=options) as driver:
        driver.get(f"file:///{html_file}")
        # Locate job opening blocks
        job_blocks = driver.find_elements(By.CSS_SELECTOR, "div.tab-pane")

        job_listings = []
        # Inspect each job block for job titles and URLs
        for block in job_blocks:
            job_titles = block.find_elements(By.CSS_SELECTOR, "h3 strong")
            # The URLs are possibly in the same h3 block as the strong element, but we need to get them from <a> elements
            a_elements = block.find_elements(By.CSS_SELECTOR, "h3 a")

            for title_element, a_element in zip(job_titles, a_elements):
                job_title = title_element.text.strip()
                job_url = a_element.get_attribute('href') if a_element else None
                job_listings.append({"Job-title": job_title, "URL": job_url})


    return json.dumps(job_listings)

if __name__ == "__main__":
    file_path = sys.argv[1]
    print(scrape_job_listings(file_path))
