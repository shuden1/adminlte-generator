import sys
import json
import threading
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

def main():
    # Get the target HTML file name from the command line argument
    target_html_file = sys.argv[1]

    # Initialize ChromeDriver with the specified options
    profile_folder_path = "D:\\Mind\\CRA\\AI_Experiments\\Job_Crawlers\\Peter\\adminlte-generator\\chrome_profile\\" + str(threading.get_ident())
    service = Service(executable_path=r"C:\Python3\chromedriver.exe")
    options = Options()
    options.add_argument(f"user-data-dir={profile_folder_path}")
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")

    driver = webdriver.Chrome(service=service, options=options)

    try:
        # Load the target HTML file
        driver.get(f"file:///{target_html_file}")

        # Use the selectors defined in STEP 1 to scrape job listings
        job_selectors = [
            {
                'block_selector': 'div.team-member',
                'title_selector': 'h4.team-name'
            }
        ]

        job_listings = []

        for selector in job_selectors:
            job_blocks = driver.find_elements(By.CSS_SELECTOR, selector['block_selector'])
            for job in job_blocks:
                title_element = job.find_element(By.CSS_SELECTOR, selector['title_selector'])
                link_element = job.find_element(By.TAG_NAME, 'a')
                job_listings.append({
                    "Job-title": title_element.text,
                    "URL": link_element.get_attribute('href')
                })

        # Return the job listings as JSON
        print(json.dumps(job_listings, indent=4))

    finally:
        driver.quit()

if __name__ == "__main__":
    main()
