import sys
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
import threading
import json

# Assuming the JSON parsing error in the provided instruction is adjusted for execution context.
def main(html_file):
    # Setup the webdriver
    options = webdriver.ChromeOptions()
    profile_folder_path = "D:\\Mind\\CRA\\AI_Experiments\\Job_Crawlers\\Peter\\adminlte-generator\\chrome_profile\\" + str(threading.get_ident())
    options.add_argument(f"user-data-dir={profile_folder_path}")
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    service = Service(executable_path=r"C:\Python3\chromedriver.exe")

    driver = webdriver.Chrome(service=service, options=options)

    # Open the local HTML file
    driver.get(f"file:///{html_file}")

    # Use the corrected selectors to extract job listings
    jobs = []
    job_elements = driver.find_elements(By.CSS_SELECTOR, '.vacancy')
    for job_element in job_elements:
        title_element = job_element.find_element(By.CSS_SELECTOR, 'h3')
        url = job_element.get_attribute('href')
        jobs.append({"Job-title": title_element.text, "URL": url})

    driver.quit()

    # Output the jobs in JSON format
    print(json.dumps(jobs))

if __name__ == "__main__":
    html_file = sys.argv[1]  # HTML file supplied as command-line argument
    main(html_file)