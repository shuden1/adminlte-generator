import sys
import threading
from selenium import webdriver
import os
from dotenv import load_dotenv

load_dotenv()
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service

def scrape_job_listings(html_file):
    profile_folder_path = os.getenv("CHROME_PROFILE_PATH") + "\\" + str(threading.get_ident())
    options = webdriver.ChromeOptions()
    options.add_argument(f"user-data-dir={profile_folder_path}")
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    service = Service(executable_path=r""+os.getenv("CHROME_DRIVER_PATH")+"")
    driver = webdriver.Chrome(service=service, options=options)
    driver.get(f"file:///{html_file}")
    job_titles = driver.find_elements(By.CSS_SELECTOR, "h2>a, .job-listing h3>a")  # Adjusted based on common job listing structures
    urls = [title.get_attribute("href") for title in job_title]
    results = [{"Job-title": title.text, "URL": url} for title, url in zip(job_titles, urls)]
    driver.quit()
    return results

if __name__ == "__main__":
    html_file = sys.argv[1]
    job_listings = scrape_job_listings(html_file)
    print(job_listings)
