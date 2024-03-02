import json
import shutil
import sys
import threading
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service

# The scraping script adjusted for a generic scenario
def scrape_job_listings(html_file_name):
    # Initialize Chrome in headless mode with a specific profile path
    profile_folder_path = "D:\\Mind\\CRA\\AI_Experiments\\Job_Crawlers\\Peter\\adminlte-generator\\chrome_profile\\" + str(threading.get_ident())
    service = Service(executable_path=r"C:\Python3\chromedriver.exe")

    options = webdriver.ChromeOptions()
    options.add_argument(f'user-data-dir={profile_folder_path}')
    options.add_argument('--headless')

    driver = webdriver.Chrome(service=service, options=options)
    driver.get(f'file:///{html_file_name}')

    # Selectors identified from BeautifulSoup analysis
    job_block_selector = 'a.ls-header-menu-secondary-nav-link'  # Selector for job listing blocks
    job_title_selector = 'a.ls-header-menu-secondary-nav-link'  # Selector for job titles and URLs

    # Scraping job listings
    job_listings = []
    for job_block in driver.find_elements(By.CSS_SELECTOR, job_block_selector):
        if "jobs" in job_block.get_attribute('href'):
            job_title = job_block.text
            job_url = job_block.get_attribute('href')
            job_listings.append({"Job-title": job_title, "URL": job_url})

    driver.quit()

    # Cleanup: Remove the profile folder
    # shutil.rmtree(profile_folder_path, ignore_errors=True)

    return json.dumps(job_listings)

if __name__ == "__main__":
    html_file_name = sys.argv[1]  # The HTML file name is passed as a command-line argument
    print(scrape_job_listings(html_file_name))
