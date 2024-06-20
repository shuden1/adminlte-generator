import sys
import json
import threading
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

def main():
    # Get the target HTML file name from the console command argument
    target_html_file = sys.argv[1]

    # Initialize ChromeDriver with the specified options
    profile_folder_path = f"D:\\Mind\\CRA\\AI_Experiments\\Job_Crawlers\\Peter\\adminlte-generator\\chrome_profile\\{str(threading.get_ident())}"
    service = Service(executable_path=r"C:\Python3\chromedriver.exe")
    options = Options()
    options.add_argument(f"user-data-dir={profile_folder_path}")
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")

    driver = webdriver.Chrome(service=service, options=options)

    # Load the target HTML file
    driver.get(f"file:///{target_html_file}")

    # Use the selectors defined in STEP 1 to scrape all job listings
    job_opening_selector = 'a.button.positioning.w-button, a.button.positioning.dark.w-button'
    job_elements = driver.find_elements(By.CSS_SELECTOR, job_opening_selector)

    job_postings = []
    for element in job_elements:
        parent_div = element.find_element(By.XPATH, '..')
        job_title = parent_div.text.replace('Apply', '').replace('Sign up', '').strip()
        job_url = element.get_attribute('href')
        if job_title:  # Ensure job title is not empty
            job_postings.append({"Job-title": job_title, "URL": job_url})

    # Close the driver
    driver.quit()

    # Return the job postings as JSON
    print(json.dumps(job_postings, indent=4))

if __name__ == "__main__":
    main()