from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
import shutil
import threading
import json
import sys

def scrape_jobs(file_name):
    # Setup Chrome options
    profile_folder_path = "D:\\Mind\\CRA\\AI_Experiments\\Job_Crawlers\\Peter\\adminlte-generator\\chrome_profile\\" + str(threading.get_ident())
    service = Service(executable_path=r"C:\Python3\chromedriver.exe")
    options = webdriver.ChromeOptions()
    options.add_argument(f"user-data-dir={profile_folder_path}")
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")

    # Initialize the driver
    driver = webdriver.Chrome(service=service, options=options)

    # Open the local HTML file
    driver.get(f"file:///{file_name}")

    # Select and process the job listings
    job_listings = []
    jobs = driver.find_elements(By.CSS_SELECTOR, "article.job_listing>a")
    for job in jobs:
        job_title = job.get_attribute("title")
        job_url = job.get_attribute("href")
        if job_title and job_url:
            job_listings.append({"Job-title": job_title, "URL": job_url})

    driver.quit()

    # Attempt to remove the profile directory
    # shutil.rmtree(profile_folder_path, ignore_errors=True)

    return json.dumps(job_listings)

if __name__ == "__main__":
    # Filename should be passed as an argument to the script
    if len(sys.argv) > 1:
        file_name = sys.argv[1]
        print(scrape_jobs(file_name))
    else:
        print("Error: Please provide the HTML file name as an argument.")
