import sys
import json
import threading
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

def scrape_jobs(file_path):
    # Initialize Chrome options
    profile_folder_path = "D:\\Mind\\CRA\\AI_Experiments\\Job_Crawlers\\Peter\\adminlte-generator\\chrome_profile\\" + str(threading.get_ident())
    options = Options()
    options.add_argument(f"user-data-dir={profile_folder_path}")
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")

    # Initialize Chrome service
    service = Service(executable_path=r"C:\Python3\chromedriver.exe")

    # Initialize WebDriver
    driver = webdriver.Chrome(service=service, options=options)

    # Load the HTML file
    driver.get(f"file:///{file_path}")

    # Selectors for job openings, titles, and URLs
    job_blocks_selector = 'a.job-box-link'
    job_title_selector = 'div.jb-title'
    job_url_attribute = 'href'

    # Find job blocks
    job_blocks = driver.find_elements(By.CSS_SELECTOR, job_blocks_selector)

    # Extract job titles and URLs
    job_data = []
    for block in job_blocks:
        try:
            title_element = block.find_element(By.CSS_SELECTOR, job_title_selector)
            job_title = title_element.text.strip()
            job_url = block.get_attribute(job_url_attribute)
            if job_title:  # Ensure job title is not empty
                job_data.append({"Job-title": job_title, "URL": job_url})
        except Exception as e:
            continue

    # Close the WebDriver
    driver.quit()

    # Return job data as JSON
    return json.dumps(job_data, indent=4)

if __name__ == "__main__":
    file_path = sys.argv[1]
    print(scrape_jobs(file_path))
