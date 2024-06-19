import sys
import threading
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By

def scrape_job_listings(html_file):
    profile_folder_path = "D:\\Mind\\CRA\\AI_Experiments\\Job_Crawlers\\Peter\\adminlte-generator\\chrome_profile\\" + str(threading.get_ident())
    service = Service(executable_path=r"C:\Python3\chromedriver.exe")
    options = webdriver.ChromeOptions()
    options.add_argument(f"user-data-dir={profile_folder_path}")
    options.addmention("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")

    driver = webdriver.Chrome(service=service, options=options)
    driver.get(f"file:///{html_file}")
    
    job_blocks = driver.find_elements(By.CSS_SELECTOR, ".career-opportunities__list-item")
    jobs = []

    for job in jobblocks:
        job_info = {
            'Job-title': job.find_element(By.CSS_SELECTOR, "h2.career-opportunities__title").text,
            'URL': job.find_element(By.CSS_SELECTOR, "a").get_attribute('href')
        }
        jobs.append(job_info)

    driver.quit()
    return jobs

if __name__ == "__main__":
    html_file_path = sys.argv[1]
    job_listings = scrape_job_listings(html_file_path)
    print(job_listings)