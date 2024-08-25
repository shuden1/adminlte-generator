from selenium import webdriver
import os
from dotenv import load_dotenv

load_dotenv()
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
import threading, sys, json

def scrape_job_listings(html_file_name):
    # Initialising WebDriver with options
    profile_folder_path = os.getenv("CHROME_PROFILE_PATH") + os.path.sep + str(threading.get_ident())
    options = webdriver.ChromeOptions()
    options.add_argument(f"user-data-dir={profile_folder_path}")
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    service = ChromeService(executable_path=r""+os.getenv("CHROME_DRIVER_PATH")+"")

    driver = webdriver.Chrome(service=service, options=options)

    # Navigate to the URL
    driver.get(f"file:///{html_file_name}")

    # Selecting the job listings using CSS Selectors identified
    job_listings = driver.find_elements(By.CSS_SELECTOR, ".careers-posts-blocks .career-post-item")

    # Extracting job titles and URLs
    jobs_json = []
    for job in job_listings:
        title_element = job.find_element(By.CSS_SELECTOR, ".testimonials-title")
        url_element = job.find_element(By.CSS_SELECTOR, "a")
        jobs_json.append({"Job-title": title_element.text, "URL": url_element.get_attribute('href')})

    driver.quit()

    # Returning JSON
    return json.dumps(jobs_json)

if __name__ == "__main__":
    file_name = sys.argv[1]  # Taking the HTML file name as an argument from external source
    print(scrape_job_listings(file_name))
