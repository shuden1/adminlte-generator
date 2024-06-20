import sys
import json
import threading
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

def scrape_jobs(file_path):
    # Initialize Chrome options
    profile_folder_path = f"D:\\Mind\\CRA\\AI_Experiments\\Job_Crawlers\\Peter\\adminlte-generator\\chrome_profile\\{str(threading.get_ident())}"
    chrome_options = Options()
    chrome_options.add_argument(f"user-data-dir={profile_folder_path}")
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")

    # Initialize Chrome service
    service = Service(executable_path=r"C:\Python3\chromedriver.exe")

    # Initialize WebDriver
    driver = webdriver.Chrome(service=service, options=chrome_options)

    try:
        # Load the HTML file
        driver.get(f"file:///{file_path}")

        # Selectors
        job_block_selector = 'li.kb-query-item'
        job_title_selector = 'h2.kt-adv-heading14_158b32-36'
        job_url_selector = 'a[href]'

        # Find job blocks
        job_blocks = driver.find_elements(By.CSS_SELECTOR, job_block_selector)

        # Extract job titles and URLs
        job_postings = []
        for job in job_blocks:
            title_element = job.find_element(By.CSS_SELECTOR, job_title_selector)
            url_element = job.find_element(By.CSS_SELECTOR, job_url_selector)
            title = title_element.text.strip()
            url = url_element.get_attribute('href')
            job_postings.append({"Job-title": title, "URL": url})

        # Return job postings as JSON
        return json.dumps(job_postings, indent=4)

    finally:
        driver.quit()

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script.py <path_to_html_file>")
        sys.exit(1)

    file_path = sys.argv[1]
    result = scrape_jobs(file_path)
    print(result)