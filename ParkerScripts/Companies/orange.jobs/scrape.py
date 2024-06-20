import sys
import json
import threading
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

def main():
    # Get the HTML file name from the command line argument
    html_file = sys.argv[1]

    # Initialize the headless Chrome WebDriver
    profile_folder_path = "D:\\Mind\\CRA\\AI_Experiments\\Job_Crawlers\\Peter\\adminlte-generator\\chrome_profile\\" + str(threading.get_ident())
    service = Service(executable_path=r"C:\Python3\chromedriver.exe")
    options = Options()
    options.add_argument(f"user-data-dir={profile_folder_path}")
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")

    driver = webdriver.Chrome(service=service, options=options)

    # Load the HTML file
    driver.get(f"file:///{html_file}")

    # Scrape job listings using the defined selectors
    job_blocks = driver.find_elements(By.CSS_SELECTOR, 'div[class*="job"]')
    job_listings = []

    for job_block in job_blocks:
        job_title_element = job_block.find_element(By.CSS_SELECTOR, 'a[class*="job-title"]')
        job_title = job_title_element.text
        job_url = job_title_element.get_attribute('href')
        job_listings.append({"Job-title": job_title, "URL": job_url})

    # Close the WebDriver
    driver.quit()

    # Print the JSON result
    print(json.dumps(job_listings, indent=4))

if __name__ == "__main__":
    main()
