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

    # Initialize the headless Chrome WebDriver
    profile_folder_path = "D:\\Mind\\CRA\\AI_Experiments\\Job_Crawlers\\Peter\\adminlte-generator\\chrome_profile\\" + str(threading.get_ident())
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

        # Use the selectors defined in STEP 1 to scrape job listings
        job_opening_selector = 'a[href^="/careers/"]'
        job_elements = driver.find_elements(By.CSS_SELECTOR, job_opening_selector)

        job_listings = []
        for job_element in job_elements:
            job_title = job_element.text.strip()
            job_url = job_element.get_attribute('href')
            job_listings.append({"Job-title": job_title, "URL": job_url})

        # Return the JSON with all job postings
        print(json.dumps(job_listings, indent=4))

    finally:
        driver.quit()

if __name__ == "__main__":
    main()
