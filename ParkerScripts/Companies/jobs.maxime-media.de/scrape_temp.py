import sys
import json
import threading
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

def main():
    # Get the HTML file name from the command line argument
    html_file_path = sys.argv[1]

    # Initialize ChromeDriver with headless options and user profile
    profile_folder_path = f"D:\\Mind\\CRA\\AI_Experiments\\Job_Crawlers\\Peter\\adminlte-generator\\chrome_profile\\{str(threading.get_ident())}"
    service = Service(executable_path=r"C:\Python3\chromedriver.exe")
    options = Options()
    options.add_argument(f"user-data-dir={profile_folder_path}")
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")

    driver = webdriver.Chrome(service=service, options=options)

    try:
        # Load the HTML file
        driver.get(f"file:///{html_file_path}")

        # Selectors for job blocks, job titles, and URLs
        job_block_selector = 'div[class*="job"], ul[class*="job"] > li, div[class*="career"], ul[class*="career"] > li'
        job_title_selector = 'a, h2 a, h3 a, p a'

        # Find all job blocks
        job_blocks = driver.find_elements(By.CSS_SELECTOR, job_block_selector)

        # Extract job titles and their associated URLs
        job_postings = []
        for block in job_blocks:
            title_element = block.find_element(By.CSS_SELECTOR, job_title_selector)
            job_postings.append({
                "Job-title": title_element.text,
                "URL": title_element.get_attribute("href")
            })

        # Print the job postings as JSON
        print(json.dumps(job_postings, indent=4))

    finally:
        driver.quit()

if __name__ == "__main__":
    main()