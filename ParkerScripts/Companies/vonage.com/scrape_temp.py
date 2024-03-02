import sys
import json
import shutil
import threading
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Step 2: Selenium script
def scrape_job_listings(html_file_name):
    profile_folder_path = "D:\\Mind\\CRA\\AI_Experiments\\Job_Crawlers\\Peter\\adminlte-generator\\chrome_profile\\" + str(threading.get_ident())

    # Set up Chrome options
    options = webdriver.ChromeOptions()
    options.add_argument(f"user-data-dir={profile_folder_path}")
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")

    # Set up Chrome service
    service = ChromeService(executable_path=r"C:\Python3\chromedriver.exe")

    # Initialize the WebDriver
    driver = webdriver.Chrome(service=service, options=options)

    # Load the provided HTML file
    driver.get("file://" + html_file_name)

    # Wait for the page to load
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, 'body')))

    # Scrape the job listings
    job_listings = []
    job_blocks = driver.find_elements(By.CSS_SELECTOR, 'li.job-listing, div.job-listing')
    for job_block in job_blocks:
        titles = job_block.find_elements(By.CSS_SELECTOR, 'h2 a, h3 a, h4 a, .job-title a')
        for title in titles:
            job_listings.append({"Job-title": title.text.strip(), "URL": title.get_attribute('href')})

    # Quit the webdriver
    driver.quit()

    # Remove the profile folder


    # Return the results in JSON format
    return json.dumps(job_listings, ensure_ascii=False)

# The actual argument for the HTML file will be supplied from an external source, as per the instructions.
html_file_argument = sys.argv[1]  # The first command line argument
print(scrape_job_listings(html_file_argument))
