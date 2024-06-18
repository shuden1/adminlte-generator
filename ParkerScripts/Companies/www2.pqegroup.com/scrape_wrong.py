import sys
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
import threading
import json

# Get the target HTML file name from the argument
target_html_file = sys.argv[1]

def scrape_job_listings():
    # Initialize the WebDriver with options
    profile_folder_path = "D:\\Mind\\CRA\\AI_Experiments\\Job_Crawlers\\Peter\\adminlte-generator\\chrome_profile\\" + str(threading.get_ident())
    service = ChromeService(executable_path=r"C:\Python3\chromedriver.exe")
    options = webdriver.ChromeOptions()
    options.add_argument(f"user-data-dir={profile_folder_path}")
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")

    driver = webdriver.Chrome(service=service, options=options)

    # Open the target HTML file
    driver.get(f"file:///{target_html_file}")

    # Scrape job listings
    job_blocks = driver.find_elements(By.CSS_SELECTOR, ".list-group-item.list-group-item-action")
    job_listings = []

    # Adjust to handle cases where job_blocks might not directly contain an <a> tag or the structure is different
    for job in jobblocks:
        try:
            a_tag = job.find_element(By.CSS_SELECTOR, 'a')
        except:
            continue
        job_title = a_tag.text.strip() if a_tag else 'No Title'
        job_url = a_tag.get_attribute('href') if a_tag else '#'

        job_listings.append({"Job-title": job_title, "URL": job_url})

    driver.quit()

    return job_listings

# Scrape and print out the job listings in JSON format
if __name__ == "__main__":
    print(json.dumps(scrape_job_listings(), indent=2))