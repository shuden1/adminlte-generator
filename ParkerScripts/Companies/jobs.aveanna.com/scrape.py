import sys
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
import threading
import json



def scrape_job_listings(html_file_name):
    # Initiate webdriver options
    options = webdriver.ChromeOptions()
    profile_folder_path = "D:\\Mind\\CRA\\AI_Experiments\\Job_Crawlers\\Peter\\adminlte-generator\\chrome_profile\\" + str(threading.get_ident())
    options.add_argument(f"user-data-dir={profile_folder_path}")
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    service = ChromeService(executable_path=r"C:\Python3\chromedriver.exe")
    
    # Start webdriver
    driver = webdriver.Chrome(service=service, options=options)
    
    driver.get(f"file:///{html_file_name}")
    
    job_listings = []
    
    # Find job titles and URLs using the defined selectors
    for job_block in driver.find_elements(By.CSS_SELECTOR, ".results-content > div"):
        job_title = job_block.find_element(By.CSS_SELECTOR, "h3").text
        job_url = job_block.find_element(By.CSS_SELECTOR, "a").get_attribute('href')
        job_listings.append({"Job-title": job_title, "URL": job_url})
    
    driver.quit()
    
    # Return the results in JSON format
    return json.dumps(job_listings)


if __name__ == "__main__":
    html_file_name = sys.argv[1]
    print(scrape_job_listings(html_file_name))