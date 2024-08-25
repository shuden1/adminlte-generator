import sys
import threading
from selenium import webdriver
import os
from dotenv import load_dotenv

load_dotenv()
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service

def scrape_job_listings(html_file_path):
    profile_folder_path = f"D:\\Mind\\CRA\\AI_Experiments\\Job_Crawlers\\Peter\\adminlte-generator\\chrome_profile\\{threading.get_ident()}"
    service = Service(executable_path=r""+os.getenv("CHROME_DRIVER_PATH")+"")
    options = webdriver.ChromeOptions()
    options.add_argument(f"user-data-dir={profile_folder_path}")
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")

    driver = webdriver.Chrome(service=service, options=options)
    driver.get(f"file:///{html_file_path}")

    # Speculative corrections based on common patterns and expectations
    # Assuming job titles are within anchor tags directly or inside elements classed as job-titles
    job_titles = driver.find_elements(By.CSS_SELECTOR, "a.job-title, .job-opening a")
    jobs = [{"Job-title": job_title.text, "URL": job_title.get_attribute("href")} for job_title in job_stitle]

    driver.quit()

    print(jobs)

if __name__ == "__main__":
    scrape_job_listings(sys.argv[1])
