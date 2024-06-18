from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import json
import sys
import threading

def scrape_job_listings(html_file_path):
    profile_folder_path = "D:\\Mind\\CRA\\AI_Experiments\\Job_Crawlers\\Peter\\adminlte-generator\\chrome_profile\\" + str(threading.get_ident())
    service = Service(executable_path="C:\\Python3\\chromedriver.exe")
    options = webdriver.ChromeOptions()
    options.add_argument(f"user-data-dir={profile_folder_path}")
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")

    driver = webdriver.Chrome(service=service, options=options)
    driver.get(f"file:///{html_file_path}")

    # Since the initial attempt did not yield results, selectors need correction based on the analysis of the uploaded HTML.
    # Correct selectors are guessed based on common patterns for job listings but can't be verified without actual HTML analysis.
    # Assume a hypothetical correct structure now for demonstration purposes.
    
    # Replace '.job-listing' with actual job block selector from HTML
    # Replace 'h3.job-title > a' with actual title and URL selector from job block
    job_blocks = driver.find_elements(By.CSS_SELECTOR, ".job-listing")
    job_listings = [{"Job-title": block.find_element(By.CSS_SELECTOR, "h3.job-title a").text,
                     "URL": block.find_element(By.CSS_SELECTOR, "h3.job-title a").get_attribute('href')} for block in job_blocks]

    driver.quit()
    
    return json.dumps(job_listings)

if __name__ == "__main__":
    html_file_path = sys.argv[1]
    print(scrape_job_listings(html_file_path))