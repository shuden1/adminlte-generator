import sys
import json
import threading
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

def main(file_path):
    # Set up Chrome options
    profile_folder_path = "D:\\Mind\\CRA\\AI_Experiments\\Job_Crawlers\\Peter\\adminlte-generator\\chrome_profile\\" + str(threading.get_ident())
    service = Service(executable_path=r"C:\Python3\chromedriver.exe")
    options = Options()
    options.add_argument(f"user-data-dir={profile_folder_path}")
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")

    # Initialize the WebDriver
    driver = webdriver.Chrome(service=service, options=options)

    # Load the HTML file
    driver.get(f"file:///{file_path}")

    # Define the selectors for job blocks, titles, and URLs
    job_blocks_selector = 'div[class*="job"], ul[class*="job"], div[class*="career"], ul[class*="career"], div[class*="opening"], ul[class*="opening"]'
    job_title_selector = 'a'

    # Find all job opening blocks
    job_blocks = driver.find_elements(By.CSS_SELECTOR, job_blocks_selector)

    # Extract job titles and URLs from the job opening blocks
    job_openings = []
    for block in job_blocks:
        title_tags = block.find_elements(By.CSS_SELECTOR, job_title_selector)
        for title_tag in title_tags:
            job_title = title_tag.text.strip()
            job_url = title_tag.get_attribute('href')
            job_openings.append({"Job-title": job_title, "URL": job_url})

    # Close the WebDriver
    driver.quit()

    # Print the result as JSON
    print(json.dumps(job_openings, indent=4))

if __name__ == "__main__":
    main(sys.argv[1])
