import sys
import json
import threading
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

def main():
    # Get the target HTML file name from the command line argument
    html_file_path = sys.argv[1]

    # Set up the ChromeDriver service and options
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
    driver.get(f"file:///{html_file_path}")

    # Use the selectors defined in STEP 1 to scrape job listings
    job_blocks = driver.find_elements(By.CSS_SELECTOR, 'div.sc-6exb5d-2.ftcjTl')
    job_data = []

    for block in job_blocks:
        title_element = block.find_element(By.CSS_SELECTOR, 'a.sc-6exb5d-1.jKkGaT')
        job_title = title_element.text.strip()
        job_url = title_element.get_attribute('href')
        job_data.append({"Job-title": job_title, "URL": job_url})

    # Close the WebDriver
    driver.quit()

    # Print the job data as JSON
    print(json.dumps(job_data, indent=4))

if __name__ == "__main__":
    main()
