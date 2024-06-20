import sys
import json
import threading
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

def scrape_jobs(file_path):
    # Profile folder path
    profile_folder_path = "D:\\Mind\\CRA\\AI_Experiments\\Job_Crawlers\\Peter\\adminlte-generator\\chrome_profile\\" + str(threading.get_ident())

    # ChromeDriver service
    service = Service(executable_path=r"C:\Python3\chromedriver.exe")

    # Chrome options
    options = Options()
    options.add_argument(f"user-data-dir={profile_folder_path}")
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")

    # Initialize WebDriver
    driver = webdriver.Chrome(service=service, options=options)

    # Open the HTML file
    driver.get(f"file:///{file_path}")

    # Selectors for job openings
    job_opening_selector = '.job'  # General selector for job blocks
    job_title_selector = '.link-title.job-title'  # Selector for job titles
    job_url_selector = 'a.job-link-wrapper'  # Selector for job URLs

    # Find job openings
    job_elements = driver.find_elements(By.CSS_SELECTOR, job_opening_selector)
    job_listings = []

    for job_element in job_elements:
        try:
            title_element = job_element.find_element(By.CSS_SELECTOR, job_title_selector)
            url_element = job_element.find_element(By.CSS_SELECTOR, job_url_selector)
            job_title = title_element.text
            job_url = url_element.get_attribute('href')
            if job_title and job_url:
                job_listings.append({"Job-title": job_title, "URL": job_url})
        except:
            continue

    # Close the WebDriver
    driver.quit()

    # Return job listings as JSON
    return json.dumps(job_listings, ensure_ascii=False)

if __name__ == "__main__":
    file_path = sys.argv[1]
    print(scrape_jobs(file_path))
