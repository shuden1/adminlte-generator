import sys
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
import threading

def scrape_job_listings(html_file_path):
    options = Options()
    profile_folder_path="D:\\Mind\\CRA\\AI_Experiments\\Job_Crawlers\\Peter\\adminlte-generator\\chrome_profile\\"+str(threading.get_ident())
    options.add_argument(f"user-data-dir={profile_folder_path}")
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")

    service = ChromeService(executable_path=r"C:\Python3\chromedriver.exe")
    driver = webdriver.Chrome(service=service, options=options)
    driver.get(f"file:///{html_file_path}")

    job_listings = []
    job_blocks = driver.find_elements(By.CSS_SELECTOR, ".job-listing, .job-opening")
    for job_block in job_blocks:
        title_elements = job_block.find_elements(By.CSS_SELECTOR, "h2 a, h3 a")
        for title_element in title_elements:
            job_title = title_element.text.strip()
            job_url = title_element.get_attribute('href').strip()
            job_listings.append({"Job-title": job_title, "URL": job_url})

    driver.quit()
    return json.dumps(job_listings, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    html_file_path = sys.argv[1]
    scraped_data = scrape_job_listings(html_file_path)
    print(scraped_data)